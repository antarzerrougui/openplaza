from django.db import models,DatabaseError
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class CategoryManager(models.Manager):
    """ Category Manager """
    use_for_related_fields = True

    def rebuild(self, focus = False):
        """ Rebuild Category Path """
        nodes = self.get_query_set().order_by('parent_id')
        self.get_query_set().filter(parent_node_id = 0).update(lft = 0, rgt = 0)
        for node in nodes:
            if focus and not node.parent_node_id :
                node.lft = 1
                node.rgt = 2
                node.save()
                focus = False
                continue
            if not focus:
                node.save()



class Category(models.Model):
    """ Category Model """
    name = models.CharField(_('Name'),max_length = 254)
    slug = models.SlugField(_('Url'))
    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children')
    lft = models.IntegerField(_('Category Path LFT'), editable=False, default = 0)
    rgt = models.IntegerField(_('Category Path RGT'), editable=False, default = 0)
    level = models.IntegerField(_('Category Tree Level'), editable=False,default = 0)
    children_count = models.IntegerField(_('Child Count'), editable=False,default = 0)
    sort_order = models.SmallIntegerField(_('Sort Order'),default= 0)
    is_active = models.BooleanField(_('Is Active'),default = False)
    description = models.TextField(_('Description'),blank=True)
    meta_title = models.CharField(_('Meta Title'),max_length = 254,blank=True)
    meta_keyword = models.CharField(_('Meta Keyword'),max_length = 254,blank=True)
    meta_description = models.CharField(_('Meta Description'),max_length = 254,blank=True)
    thumbnail = models.ImageField(_('Thumbnail'),upload_to = settings.MEDIA_ROOT,max_length = 254,blank=True)
    image = models.ImageField(_('Image'),upload_to = settings.MEDIA_ROOT, max_length = 254,blank=True)
    created_at = updated_at = models.DateTimeField(_('Created At'),auto_now_add= True,null=True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True,null=True,blank=True)
    objects = CategoryManager()
    class Meta:
        db_table = "category"
        verbose_name = _('Category')
        verbose_name_plural = _('Category')

    def __unicode__(self):
        return self.name


    def delete(self, using=None,children = True):
        try:
            from django.db import connection, transaction
            cursor = connection.cursor()
            instance = self._default_manager.get(pk = self.id)
            depth = instance.rgt - instance.lft + 1
            gtFilter = instance.rgt

            if children:
                query = "DELETE FROM %s WHERE lft BETWEEN %d AND %d"% (Category._meta.db_table,instance.lft,instance.rgt)
                cursor.execute(query)

                query = "UPDATE %s SET lft = lft - %d WHEdRE lft > %d"% (Category._meta.db_table,depth,gtFilter)
                cursor.execute(query)

                query = "UPDATE %s SET rgt = rgt - %d WHERE rgt > %d"% (Category._meta.db_table,depth,gtFilter)
                cursor.execute(query)

            else: # Only delete current node
                query = "DELETE FROM %s WHERE lft = %d"% (Category._meta.db_table,instance.lft)
                cursor.execute(query)

                query = "UPDATE %s SET rgt = rgt - 1,lft = lft - 1 WHERE lft BETWEEN %d AND %d"% (Category._meta.db_table,instance.lft,instance.rgt)
                cursor.execute(query)

                query = "UPDATE %s SET rgt = rgt - 2 WHERE rgt > %d"% (Category._meta.db_table,instance.rgt)
                cursor.execute(query)

                query = "UPDATE %s SET lft = lft - 2 WHERE lft > %d"% (Category._meta.db_table,instance.rgt)
                cursor.execute(query)

                query = "UPDATE %s SET parent_node_id = %d WHERE parent_node_id = %d"%(Category._meta.db_table,instance.parent_node_id,instance.id)
                cursor.execute(query)

            super(Category,self).delete(using)
        except DatabaseError as e:
            return None
        except models.ObjectDoesNotExist :
            return None
        return self.id

def pre_post_rebuild_node_level(sender, instance, **kwargs):
    #update_fields django 1.5 featured
    parent = instance.parent_id
    lft = 1
    gtFilter = None
    try :
        nodes = sender.objects.order_by("-rgt").filter(parent_id = parent).exclude(id = instance.id)
        if nodes :
            node = nodes[0]
            gtFilter = node.rgt
            lft = node.rgt + 1
        elif parent:
            node = sender.objects.get(pk = parent)
            lft = node.lft + 1
            gtFilter = node.lft
        if gtFilter :
            sender.objects.select_for_update().filter(lft__gt = gtFilter).update(lft = models.F('lft') + 2)
            sender.objects.select_for_update().filter(rgt__gt = gtFilter).update(rgt = models.F('rgt') + 2)
    except models.ObjectDoesNotExist:
         raise ValueError(_("Parent node not found."))
    rgt = lft + 1
    instance.lft = lft
    instance.rgt = rgt
    return instance

pre_save.connect(pre_post_rebuild_node_level, sender=Category)

class Product(models.Model):
    """ Product Model """
    name = models.CharField(_('Name'),max_length = 255)
    category = models.ManyToManyField(Category)
    sku =  models.CharField(_('SKU'),max_length = 255)
    price = models.DecimalField(_('Price'),max_digits = 15,decimal_places = 4)
    qty = models.IntegerField(_('Qty'), default = 0)
    weight = models.DecimalField(_('Weight'),max_digits = 15,decimal_places = 8)
    created_at = updated_at = models.DateTimeField(_('Created At'),auto_now_add= True,null=True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True,null=True,blank=True)
    sort_order = models.SmallIntegerField(_('Sort Order'),default= 0)
    is_active = models.BooleanField(_('Is Active'),default = False)
    short_description = models.TextField(_('Short Description'),blank=True)
    description = models.TextField(_('Description'),blank=True)
    meta_title = models.CharField(_('Meta Title'),max_length = 255,blank=True)
    meta_keyword = models.CharField(_('Meta Keyword'),max_length = 255,blank=True)
    meta_description = models.CharField(_('Meta Description'),max_length = 255,blank=True)
    thumbnail = models.ImageField(_('Product Thumbnail'),upload_to = settings.MEDIA_ROOT,max_length = 255,blank=True)
    slug = models.SlugField(_('Product Url'))

    class Meta:
        db_table = "product"
        verbose_name = _('Product')
        verbose_name_plural = _('Product')

    def __unicode__(self):
        return self.name
