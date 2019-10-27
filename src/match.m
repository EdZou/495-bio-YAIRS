function res = match(eyeimage_1, eyeimage_2)

[template_1, mask_1] = createiristemplate(eyeimage_1, '');
[template_2, mask_2] = createiristemplate(eyeimage_2, '');

res = gethammingdistance(template_1, mask_1, template_2, mask_2, 1)