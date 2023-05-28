def slug_generator(instance, gutter=1):
    cls = instance.__class__
    slug = instance.slug
    if not slug:
        slug = instance.title.lower().replace(" ", "-")
    while cls.objects.filter(slug= slug).exists() or slug is None:
        slug = f"{instance.title.lower().replace(' ', '-')}{gutter}"
        gutter += 1
    return slug