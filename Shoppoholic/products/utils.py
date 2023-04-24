def slug_generator(instance, gutter=1):
    cls = instance.__class__
    slug = instance.slug
    if slug is None:
        slug = instance.title.lower().replace(" ", "-")
        
    while cls.objects.filter(slug= slug).exists():
        print("Slug exists: ", slug)
        slug = f"{instance.title.lower().replace(' ', '-')}{gutter}"
        gutter += 1
        print("New Slug: ", slug)
    
    return slug