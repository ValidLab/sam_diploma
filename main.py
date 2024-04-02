from ikomia.dataprocess.workflow import Workflow
from ikomia.utils import ik
from ikomia.utils.displayIO import display

wf = Workflow()

sam = wf.add_task(ik.infer_segment_anything(
      # draw_graphic_input = True,
      model_name='vit_h',
      input_box = '[204.8, 221.8, 769.7, 928.5]'
      ),
      auto_connect=True)

sd_inpaint = wf.add_task(ik.infer_hf_stable_diffusion_inpaint(
    model_name = 'stabilityai/stable-diffusion-2-inpainting',
    prompt = 'horse, high resolution',
    negative_prompt = 'low quality',
    num_inference_steps = '100',
    guidance_scale = '7.5',
    num_images_per_prompt = '1'),
    auto_connect=True
)

wf.run_on(url="https://raw.githubusercontent.com/Ikomia-dev/notebooks/main/examples/img/img_cat.jpg")

display(sam.get_image_with_mask())
display(sd_inpaint.get_output(0).get_image())