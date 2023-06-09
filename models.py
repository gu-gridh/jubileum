# from django.db import models
from django.contrib.gis.db import models
import diana.abstract.models as abstract
from django.utils.translation import gettext_lazy as _
from diana.storages import OriginalFileStorage
from ckeditor.fields import RichTextField
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
# Create your models here.

class ImageTypeTag(abstract.AbstractTagModel):
    
    class Meta:
        verbose_name = _("Type of image")
        verbose_name_plural = _("Types of image")

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)

# Place
class Place(abstract.AbstractBaseModel):
    
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("name"), help_text=_("this field refers to the placename"))
    geometry = models.GeometryField(verbose_name=_("geometry"), blank=True, null=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text=_("Parent of this place"))
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the place"))
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Place")


class Source(abstract.AbstractBaseModel):
    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    author = models.CharField(max_length=256, blank=True, null=True)
    attribution = models.CharField(max_length=256, blank=True, null=True)
    publication_place = models.CharField(max_length=256, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    gupea = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title}"
    

class Image(abstract.AbstractTIFFImageModel):

    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    place   = models.ForeignKey(Place, null=True, blank=True, on_delete=models.CASCADE, related_name="images")
    type = models.CharField(max_length=32, null=True, blank=True, help_text=_("Type of the image can be jpeg, png, etc."))
    image_url = models.CharField(max_length=256, blank=True, null=True)
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the images"))

    def __str__(self) -> str:
        return f"{self.title}"
    

class Layer(abstract.AbstractBaseModel):
    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=32, null=True, blank=True)
    format = models.CharField(max_length=32, null=True, blank=True, help_text=_("Type of the image can be jpeg, png, etc."))
    description = RichTextField(null=True, blank=True, verbose_name=_("description"))

