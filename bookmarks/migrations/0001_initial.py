# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BookmarkTag'
        db.create_table('bookmarks_bookmarktag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('bookmarks', ['BookmarkTag'])

        # Adding model 'Bookmark'
        db.create_table('bookmarks_bookmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('meta_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=10)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('bookmarks', ['Bookmark'])

        # Adding M2M table for field tags on 'Bookmark'
        db.create_table('bookmarks_bookmark_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bookmark', models.ForeignKey(orm['bookmarks.bookmark'], null=False)),
            ('bookmarktag', models.ForeignKey(orm['bookmarks.bookmarktag'], null=False))
        ))
        db.create_unique('bookmarks_bookmark_tags', ['bookmark_id', 'bookmarktag_id'])


    def backwards(self, orm):
        # Deleting model 'BookmarkTag'
        db.delete_table('bookmarks_bookmarktag')

        # Deleting model 'Bookmark'
        db.delete_table('bookmarks_bookmark')

        # Removing M2M table for field tags on 'Bookmark'
        db.delete_table('bookmarks_bookmark_tags')


    models = {
        'bookmarks.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'meta_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bookmarks.BookmarkTag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'bookmarks.bookmarktag': {
            'Meta': {'object_name': 'BookmarkTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['bookmarks']