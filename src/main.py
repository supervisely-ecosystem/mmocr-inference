import os
from mmocr.apis import MMOCRInferencer
import supervisely as sly
import utils

device = "cuda"
batch_size = 2
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)

model = MMOCRInferencer(det="DBNetpp", rec='ABINet', device=device)

image_paths = ["demo.png"]
predictions = model(image_paths, batch_size)["predictions"]

obj_class = sly.ObjClass("text_det", sly.Rectangle, [0, 255, 0])
for pred, image_path in zip(predictions, image_paths):
    img_name, _ = os.path.splitext(os.path.basename(image_path))
    
    # save texts
    texts = pred["rec_texts"]
    sly.json.dump_json_file(texts, f"{output_dir}/{img_name}.json")

    # draw visualizations (debug)
    labels = []
    for text, text_score, rect, rect_score in zip(*list(pred.values())):
        assert len(rect) == 8
        label = utils.det_polygon_2_label(rect, obj_class)
        labels.append(label)
    img = sly.image.read(image_path)
    ann = sly.Annotation(img.shape[:2], labels)
    ann.draw_pretty(img, thickness=1)
    sly.image.write(f"{output_dir}/{img_name}_pred.jpg", img)
