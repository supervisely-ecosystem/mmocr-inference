from mmocr.apis import MMOCRInferencer
import supervisely as sly

device = "cuda"
batch_size = 2

model = MMOCRInferencer(det="DBNetpp", rec='ABINet', device=device)


predictions = model(["demo.png"], batch_size)["predictions"]

img = sly.image.read("demo.png")

obj_class = sly.ObjClass("text_det", sly.Rectangle, [0, 255, 0])

for pred in predictions:
    texts = pred["rec_texts"]
    print(texts)
    labels = []
    for text, text_score, rect, rect_score in zip(*list(pred.values())):
        # convert rectangles to sly.Rectangle
        assert len(rect) == 8
        rect = list(map(int, rect))
        x,y = rect[::2], rect[1::2]
        xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
        rect = sly.Rectangle(ymin, xmin, ymax, xmax)
        label = sly.Label(rect, obj_class)
        labels += [label]
    ann = sly.Annotation(img.shape[:2], labels)

ann.draw_pretty(img, thickness=1)

sly.image.write("demo_pred.jpg", img)
sly.json.dump_json_file(texts, "texts.json")