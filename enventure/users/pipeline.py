def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'facebook':
    	url = response.get('cover',{}).get("source","")
    if url:
        user.avatar = url
        user.save()