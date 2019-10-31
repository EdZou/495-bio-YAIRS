function res = getHD(eyeimage_1, eyeimage_2)

[template_1, mask_1] = getTemplate(eyeimage_1, '');
[template_2, mask_2] = getTemplate(eyeimage_2, '');

res = gethammingdistance(template_1, mask_1, template_2, mask_2, 1);