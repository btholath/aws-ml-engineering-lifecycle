import os
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

artifact_dir = Path("05_model_inference/model_packaging/model")
artifact_dir.mkdir(parents=True, exist_ok=True)

src_model = Path("03_model_training/model/xgboost-model")
dst_model = artifact_dir / "xgboost-model"
shutil.copy(src_model, dst_model)

logger.info(f"✅ Model artifact prepared at: {dst_model}")