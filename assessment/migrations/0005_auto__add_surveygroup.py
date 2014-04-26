# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SurveyGroup'
        db.create_table('assessment_surveygroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('assessment', ['SurveyGroup'])

        # Adding M2M table for field surveys on 'SurveyGroup'
        m2m_table_name = db.shorten_name('assessment_surveygroup_surveys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('surveygroup', models.ForeignKey(orm['assessment.surveygroup'], null=False)),
            ('survey', models.ForeignKey(orm['assessment.survey'], null=False))
        ))
        db.create_unique(m2m_table_name, ['surveygroup_id', 'survey_id'])

        # Removing M2M table for field visible_for on 'Survey'
        db.delete_table(db.shorten_name('assessment_survey_visible_for'))


    def backwards(self, orm):
        # Deleting model 'SurveyGroup'
        db.delete_table('assessment_surveygroup')

        # Removing M2M table for field surveys on 'SurveyGroup'
        db.delete_table(db.shorten_name('assessment_surveygroup_surveys'))

        # Adding M2M table for field visible_for on 'Survey'
        m2m_table_name = db.shorten_name('assessment_survey_visible_for')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('survey', models.ForeignKey(orm['assessment.survey'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['survey_id', 'group_id'])


    models = {
        'assessment.answer': {
            'Meta': {'object_name': 'Answer', 'unique_together': "(('result', 'question'),)"},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']", 'related_name': "'answers'"}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Result']", 'related_name': "'answers'"})
        },
        'assessment.choice': {
            'Meta': {'ordering': "['id']", 'object_name': 'Choice'},
            'choice_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']", 'related_name': "'choices'"})
        },
        'assessment.question': {
            'Meta': {'ordering': "['survey', 'id']", 'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'of_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']"})
        },
        'assessment.result': {
            'Meta': {'object_name': 'Result', 'unique_together': "(('survey', 'user'),)"},
            'completed_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'score_percentage': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '3'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']", 'related_name': "'results'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'results'"})
        },
        'assessment.survey': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Survey'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True'})
        },
        'assessment.surveygroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'SurveyGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'surveys': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['assessment.Survey']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assessment']