# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # ('drawing', '0003_auto__add_field_windenergysite_description'),
    ]

    def alterGeomSRID(table, column, type):
        alterSQL = """ALTER TABLE {table}
                DROP CONSTRAINT IF EXISTS enforce_srid_{column},
                ALTER COLUMN {column} TYPE geometry({type}, {srid})
                    USING ST_Transform({column},{srid}),
                ADD CONSTRAINT enforce_srid_{column} CHECK(st_srid({column}) = {srid});"""

        return migrations.RunSQL(
            alterSQL.format(table=table, column=column, type=type, srid=3857),
            alterSQL.format(table=table, column=column, type=type, srid=99996)
        )

    operations = [
        alterGeomSRID('drawing_aoi', 'geometry_orig', 'POLYGON'),
        alterGeomSRID('drawing_aoi', 'geometry_final', 'POLYGON'),
    ]
