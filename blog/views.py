from django.shortcuts import render, get_object_or_404
from . models import Post
from . forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.http import JsonResponse
from PIL import Image
import urllib.request
import io
import base64
from base64 import decodestring
# Create your views here.

class SignUpView(CreateView):
	template_name = "blog/signup.html"
	form_class = UserCreationForm

def validate_username(request):

    imgBase64 = request.POST.get("imgBase64")

    imgBase64 = imgBase64.replace('data:image/png;base64,', '')
    imgBase64 = imgBase64.replace(' ', '+')
    imgBase64 = base64.b64decode(imgBase64 + "==")


    with open("/home/sovervo/my-blog/blog/user_drawing.png", 'wb') as f:
    	f.write(imgBase64)
    img1 = Image.open("/home/sovervo/my-blog/blog/user_drawing.png")
    img1 = img1.resize((476,500), Image.ANTIALIAS)
    
    im_1_width, im_1_height = img1.size

    px = img1.load()
    for x in range(0, im_1_width):
    	for y in range(0, im_1_height):
    		if(px[x,y][0] != 255):
    			px[x,y] = 0

    img1.save("/home/sovervo/my-blog/blog/user_drawing.png")

    img = Image.open("/home/sovervo/my-blog/blog/first_image.png")

    sum_pixel = compare(img, img1)
    #count = count_pixel(img, img1)
    data = {
        'count':  sum_pixel
    }
    return JsonResponse(data)



def post_list(request):
	posts = Post.objects.all()
	return render(request, "blog/post_list.html", {"posts" : posts})

def post_detail(request, pk):
	post  = get_object_or_404(Post, pk=pk)
	return render(request, "blog/post_detail.html", {"post" : post})

def post_new(request):
	form = PostForm()
	return render(request, "blog/post_edit.html", {"form" : form})

def move_to(top, left, val, width, height, pix, matrix_im, delta):
    for x in range(0, width):
        for y in range(0, height):
            if (pix[x,y][0] == 0) & (matrix_im[y + (delta//2) + top][x + (delta//2) + left] == 0):
                matrix_im[y + (delta//2) + top][x + (delta//2) + left] = val

def compare(im, im_1):
	width, height = im.size
	delta = 10;
	deltaVal = 2;
	pix = im.load()
	pix_1 = im_1.load()

	# moved for




	matrix_im = [[0 for x in range(width + delta)] for y in range(height + delta)]
	countSum = 0
	shouldBe = 0
	# original position
	for x in range(0, width):
	    for y in range(0, height):
	        if pix[x,y][0] == 0:
	            matrix_im[y + (delta//2)][x + (delta//2)] = deltaVal


	localCount = deltaVal

	for x in range(1, deltaVal):
	    move_to(0, x, localCount, width, height, pix, matrix_im, delta)
	    move_to(0, -x, localCount, width, height, pix, matrix_im, delta)
	    move_to(x, 0, localCount, width, height, pix, matrix_im, delta)
	    move_to(-x, 0, localCount, width, height, pix, matrix_im, delta)
	    localCount -= 1


	for x in range(0, width):
	    for y in range(0, height):
	        if pix_1[x,y][0] == 0:
	            countSum += matrix_im[y + (delta//2)][x + (delta//2)]
	        if pix[x,y][0] == 0:
	            shouldBe += matrix_im[y + (delta//2)][x + (delta//2)]

	if(countSum < shouldBe):
		return str(round(countSum*100/shouldBe)) +" %"
	else:
		return str(round(countSum*100/shouldBe - 100)) +" %"

def count_pixel(im, im_1):
	width, height = im.size
	pix = im.load()
	pix_1 = im_1.load()
	pix_0_count = 0

	for x in range(0, width):
		for y in range(0, height):
			if(pix_1[x,y][2] == 0) or (pix_1[x,y][2] == 3):
				pix_0_count += 1
	return pix_0_count
