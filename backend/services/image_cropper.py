from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, Union

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - numpy is optional
    np = None  # type: ignore

from PIL import Image


BBox = Tuple[int, int, int, int]  # (x1, y1, x2, y2)


@dataclass(frozen=True)
class SavedCrop:
    output_path: Path
    bbox: BBox
    index: int


def _ensure_dir(path: Union[str, Path]) -> Path:
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _clamp_bbox(bbox: BBox, width: int, height: int) -> BBox:
    x1, y1, x2, y2 = bbox
    x1 = max(0, min(x1, width))
    y1 = max(0, min(y1, height))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def _expand_bbox(bbox: BBox, expand_ratio: float, width: int, height: int) -> BBox:
    if expand_ratio <= 0:
        return _clamp_bbox(bbox, width, height)
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    cx = x1 + w / 2
    cy = y1 + h / 2
    w_new = w * (1 + expand_ratio)
    h_new = h * (1 + expand_ratio)
    x1_new = int(round(cx - w_new / 2))
    y1_new = int(round(cy - h_new / 2))
    x2_new = int(round(cx + w_new / 2))
    y2_new = int(round(cy + h_new / 2))
    return _clamp_bbox((x1_new, y1_new, x2_new, y2_new), width, height)


def _to_pil(image: Union[str, Path, Image.Image, "np.ndarray"]) -> Image.Image:
    if isinstance(image, Image.Image):
        return image
    if np is not None and hasattr(image, "shape"):
        arr = image
        if arr.ndim == 2:
            return Image.fromarray(arr)
        if arr.ndim == 3 and arr.shape[2] in (3, 4):
            return Image.fromarray(arr)
    # assume path-like
    return Image.open(image).convert("RGB")


def crop_boxes(
    image: Union[str, Path, Image.Image, "np.ndarray"],
    boxes_xyxy: Sequence[BBox],
    *,
    expand_ratio: float = 0.0,
) -> List[Image.Image]:
    """
    Crop multiple regions from an image using (x1, y1, x2, y2) boxes.

    - image can be a file path, PIL.Image, or numpy array (HWC, RGB).
    - expand_ratio expands each box by the given fraction before clamping.
    """
    pil_img = _to_pil(image)
    width, height = pil_img.size
    crops: List[Image.Image] = []
    for bbox in boxes_xyxy:
        x1, y1, x2, y2 = _expand_bbox(bbox, expand_ratio, width, height)
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            continue
        crops.append(pil_img.crop((x1, y1, x2, y2)))
    return crops


def save_crops(
    image: Union[str, Path, Image.Image, "np.ndarray"],
    boxes_xyxy: Sequence[BBox],
    output_dir: Union[str, Path],
    *,
    base_name: Optional[str] = None,
    image_format: str = "jpg",
    expand_ratio: float = 0.0,
) -> List[SavedCrop]:
    """
    Crop and save regions to output_dir. Returns paths and metadata for saved crops.

    - base_name: base filename for crops; defaults to source file stem or "crop".
    - image_format: file extension/format, e.g., "jpg", "png".
    - expand_ratio: expand each bbox before clamping and cropping.
    """
    output_path = _ensure_dir(output_dir)
    pil_img = _to_pil(image)

    if base_name is None:
        if isinstance(image, (str, Path)):
            base_name = Path(image).stem
        else:
            base_name = "crop"

    width, height = pil_img.size
    saved: List[SavedCrop] = []
    for idx, bbox in enumerate(boxes_xyxy):
        x1, y1, x2, y2 = _expand_bbox(bbox, expand_ratio, width, height)
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            continue
        crop_img = pil_img.crop((x1, y1, x2, y2))
        filename = f"{base_name}_crop_{idx:03d}.{image_format.lower()}"
        dest = output_path / filename
        crop_img.save(dest)
        saved.append(SavedCrop(output_path=dest, bbox=(x1, y1, x2, y2), index=idx))
    return saved


def crop_single(
    image: Union[str, Path, Image.Image, "np.ndarray"],
    bbox_xyxy: BBox,
    *,
    expand_ratio: float = 0.0,
) -> Optional[Image.Image]:
    pil_img = _to_pil(image)
    width, height = pil_img.size
    x1, y1, x2, y2 = _expand_bbox(bbox_xyxy, expand_ratio, width, height)
    if x2 - x1 <= 0 or y2 - y1 <= 0:
        return None
    return pil_img.crop((x1, y1, x2, y2))


