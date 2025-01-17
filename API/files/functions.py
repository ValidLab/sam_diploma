import requests

from typing import List

from fastapi import Cookie

from ikomia.utils import ik
from ikomia.utils.displayIO import display
from ikomia.dataprocess.workflow import Workflow


def reformate_photo(path: str, input_box: List[str], prompt: str, anti_prompt: str):
    print(input_box)
    wf = Workflow()

    inp = '['
    for coor in input_box[:-1]:
        inp = inp + coor + ', '
    inp = inp + input_box[-1] + ']'

    sam = wf.add_task(ik.infer_segment_anything(
        # draw_graphic_input = True,  # use this
        model_name='vit_h',
        input_box=inp  # if str draw_graphic_input don't use this one
        ),
        auto_connect=True)

    sd_inpaint = wf.add_task(ik.infer_hf_stable_diffusion_inpaint(
        model_name='stabilityai/stable-diffusion-2-inpainting',
        prompt=prompt,  # add an opportunity to rewrite prompt
        negative_prompt=anti_prompt,
        num_inference_steps='100',
        guidance_scale='7.5',
        num_images_per_prompt='1'),
        auto_connect=True
    )

    wf.run_on(path=path)  # add photo
    display(sam.get_image_with_mask())
    display(sd_inpaint.get_output(0).get_image())
    return sd_inpaint.get_output(0).get_image()  # add a save mechanism


def check_auth(fastapiusersauth: str = Cookie(None)):
    response = requests.get("http://localhost:8001/api/user/get_user_info", cookies={"fastapiusersauth": fastapiusersauth})
    return response.status_code, response.json()
