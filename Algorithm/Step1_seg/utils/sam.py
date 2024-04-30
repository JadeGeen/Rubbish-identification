from segment_anything import sam_model_registry, build_sam, SamPredictor ,SamAutomaticMaskGenerator

sam_checkpoint = "/disk2/zhanglingming/trashcls/SAM_test/checkpoint/sam_vit_h_4b8939.pth"
model_type = "vit_h"

device = "cuda"


class SamModel():
    def __init__(self,model_type, sam_checkpoint,device):
        super().__init__(sam_checkpoint)
        self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam.to(device=device)
        self.predictor = SamPredictor(self.sam)
        self.automatic_mask_generator = SamAutomaticMaskGenerator(self.sam)

    def predict(self, image, input_point, input_label):
        self.predictor.set_image(image)
        
        masks, scores, logits = self.predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )
        
        return masks, scores, logits
    
    def generate_mask(self, image):
        return self.automatic_mask_generator.generate(image)

# def maskToBoxes(mask)