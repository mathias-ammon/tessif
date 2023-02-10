# tessif/frused/themes.py
# -*- coding: utf-8 -*-
"""
:mod:`~tessif.frused.themes` is a :mod:`tessif` subpackage grouping color and
hatch themes to :`tessif.frused.namedtuples.NodeColorGroupings` for convenient
and automated access.
"""
import collections
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#
from tessif.frused.namedtuples import NodeColorGroupings, Uid
import tessif.frused.spellings as spellings


colors = NodeColorGroupings(
    component=collections.OrderedDict([
        ('bus', '#9999ff'),  # websafe very light blue
        ('sink', '#9999ff'),  # websafe very light blue
        ('storage', '#9999ff'),  # websafe very light blue
        ('source', '#9999ff'),  # websafe very light blue
        ('transformer', '#9999ff'),  # websafe very light blue
        ('connector', '#9999ff'),  # websafe very light blue
    ]),
    name=collections.OrderedDict([
        ('renewables', '#00ff00'),  # websafe mostly pure lime green
        ('photovoltaic', '#ff9900'),  # websafe mostly pure orange
        ('solarthermal', '#ff0099'),  # websafe mostly pure pink
        ('onshore', '#99ccff'),  # websafe very light blue
        ('offshore', '#00ccff'),  # websafe mosty pure cyan
        ('hydro_electric', '#000099'),  # websafe dark blue
        ('combined_heat_power', '#9933cc'),  # websafe strong violet
        ('power_plant', '#ff6600'),  # websafe mostly pure orange
        ('heat_plant', '#b30000'),  # strong red
        ('electrical_line', '#ffcc00'),  # websafe mostly pure yellow
        ('gas_station', '#6633cc'),
        ('gas_pipeline', '#336666'),  # websafe very dark desaturated cyan
        ('gas_delivery', '#006666'),  # websafe very dark cyan
        ('oil_pipeline', '#666666'),  # websafe very dark grey
        ('oil_delivery', '#333333'),  # websafe even verier dark grey
        ('hydro_electrical_storage', '#0000cc'),  # websafe strong blue
        ('electro_chemical_storage', '#ccff00'),  # websafe mostly pure yellow
        ('electro_mechanical_storage', '#999900'),  # websafe dark yellow
        ('thermal_energy_storage', '#cc0033'),  # websafe strong red
        ('power2x', '#669999'),  # websafe mostly desaturated dark cyan
        ('power2heat', '#b30000'),  # strong red
        ('imported', '#ff6600'),  # websafe orange
        ('backup', '#990099'),  # websafe dark magenta
        ('demand', '#330099'),  # websafe dark violet
        ('export', '#006600'),  # websafe dark green
        ('excess', '#cc0000'),  # websafe pure red
        ('connector', '#669999'),  # websafe mostly desaturated dark cyan
    ]),
    carrier=collections.OrderedDict([
        ('solar', '#ff9900'),  # websafe mostly pure orange
        ('wind', '#00ccff'),  # websafe mosty pure cyan
        ('water', '#000099'),  # websafe dark blue
        ('biomass', '#009900'),  # websafe dark lime green
        ('gas', '#336666'),  # websafe very dark desaturated cyan
        ('oil', '#666666'),  # websafe very dark gray
        ('lignite', '#993300'),  # websafe dark orange
        ('hardcoal', '#000000'),  # websafe black
        ('nuclear', '#cccc00'),  # websafe strong yellow
        ('electricity', '#FFD700'),  # websafe pure yellow
        ('steam', '#cc0033'),  # websafe crimson
        ('hot_water', '#ff3300'),  # websafe mostly pure red
    ]),
    sector=collections.OrderedDict([
        ('power', '#ffff33'),  # websafe vivid yellow
        ('heat', '#FF0000'),  # websafe red
        ('mobility', '#669999'),  # websafe mostly desaturated dard cyan
        ('coupled', '#6633cc'),  # websafe strong violet
    ]),)
""" Tessif color themes.  Stored inside a
:attr:`~tessif.frused.namedtuples.NodeColorGroupings`
:class:`~typing.NamedTuple`. Assembled using `colorhexa
<https://www.colorhexa.com/>`_
Categorized by :attr:`~tessif.frused.namedtuples.NodeColorGroupings`

For each category there is a mapping of identifiers to colors

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    import tessif.frused.themes as themes
    import pandas
    import dutils

    for pos, dct in enumerate(themes.colors):
        category = themes.colors._fields[pos]

        path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_colors.png'.format(category))
        fig = themes._plot_colortable(
            dct, str(category),
            sort_colors=False, emptycols=0)
        fig.savefig(path)


        csv_path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}.csv'.format(category))

        df = dutils.to_dataframe(
            dct, columns=2, fillvalue='')

        df.to_csv(csv_path, header=None, index=None, na_rep='None')

|

**Component Grouped Colors:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/component.csv

.. image:: themes/component_colors.png
    :align: center
    :alt: Image showing the supported component colors

|

**Named Grouped Colors:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/name.csv
    :stub-columns: 1

.. image:: themes/name_colors.png
    :align: center
    :alt: Image showing the supported name colors

|

**Carrier Grouped Colors:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/carrier.csv
    :stub-columns: 1

.. image:: themes/carrier_colors.png
    :align: center
    :alt: Image showing the supported carrier colors

|

**Sector Grouped Colors:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/sector.csv
    :stub-columns: 1

.. image:: themes/sector_colors.png
    :align: center
    :alt: Image showing the supported sector colors
"""


cmaps = NodeColorGroupings(
    component=collections.OrderedDict([
        ('bus', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                 '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
        ('sink', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                  '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
        ('storage', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                     '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
        ('source', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                    '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
        ('transformer', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                         '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
        ('connector', ['#4d4dff', '#6666ff', '#8080ff', '#9999ff',
                       '#b3b3ff', '#ccccff', '#e6e6ff']),  # very light blue
    ]),
    carrier=collections.OrderedDict([
        ('solar', ['#ff5900', '#ff6f00', '#ff8400',
                   '#ff9900', '#ffae00', '#ffc400', '#ffd900']),  # orange
        ('wind', ['#002aff', '#008cff', '#00b7ff', '#00ccff',
                  '#00e1ff', '#00f7ff', '#00fff2']),  # cyan
        ('water', ['#00004d', '#190099', '#0d0099',
                   '#000099', '#000d99', '#001a99', '#002699']),  # dark blue
        ('biomass', ['#004d00', '#006600', '#008000', '#009900',
                     '#00b300', '#00cc00', '#00e600']),  # dark lime
        ('gas', ['#1a3333', '#224444', '#2b5555', '#336666',
                 '#3c7777', '#448888', '#4d9999']),  # dark desaturated cyan
        ('oil', ['#404040', '#4d4d4d', '#595959', '#666666',
                 '#737373', '#808080', '#8c8c8c']),  # very dark grey
        ('lignite', ['#4d1a00', '#662200', '#802b00', '#993300',
                     '#b33c00', '#cc4400', '#e64d00']),  # dark brown
        ('hardcoal', ['#000000', '#0d0d0d', '#191919', '#262626',
                      '#333333', '#404040', '#4c4c4c']),  # black
        ('nuclear', ['#808000', '#999900', '#b3b300', '#cccc00',
                     '#e6e600', '#ffff00', '#ffff1a']),  # strong yellow
        ('electricity', ['#b39700', '#ccac00', '#e6c200', '#ffd700',
                         '#ffdb1a', '#ffdf33', '#ffe34d']),  # pure yellow
        ('steam', ['#800020', '#990026', '#b3002a', '#cc0033',
                   '#e60039', '#ff0040', '#ff1a53']),  # crimson
        ('hot_water', ['#b32400', '#cc2900', '#e62e00', '#ff3300',
                       '#ff471a', '#ff5c33', '#ff704d']),  # pure red
    ]),
    sector=collections.OrderedDict([
        ('power', ['#ff5900', '#ff6f00', '#ff8400', '#ff9900',
                   '#ffae00', '#ffc400', '#ffd900']),  # vivid yellow
        ('heat', ['#b30000', '#cc0000', '#e60000',
                  '#ff0000', '#ff1a1a', '#ff3333', '#ff4d4d']),  # red
        ('mobility', ['#476b6b', '#527a7a', '#5c8a8a', '#669999', '#75a3a3',
                      '#85adad', '#94b8b8']),  # desaturated dark cyan
        ('coupled', ['#47248f', '#5229a3', '#5c2eb8', '#6633cc',
                     '#7547d1', '#855cd6', '#9470db', ]),  # strong violet
    ]),
    name=collections.OrderedDict([
        ('renewables', ['#00b300', '#00cc00', '#00e600', '#00ff00',
                        '#1aff1a', '#33ff33', '#4dff4d']),  # lime green
        ('photovoltaic', ['#b37400', '#cc8400', '#e69500', '#ffa500',
                          '#ffae1a', '#ffb733', '#ffc04d']),  # pure orange
        ('solarthermal', ['#b300b6', '#cc007a', '#e6008a', '#ff0099',
                          '#ff1aa3', '#ff33ad', '#ff4db8']),  # pure pink
        ('offshore', ['#4da6ff', '#66b3ff', '#80bfff', '#99ccff',
                      '#b3d9ff', '#cce6ff', '#e6f2ff']),  # pure cyan
        ('onshore', ['#002aff', '#008cff', '#00b7ff', '#00ccff',
                     '#00e1ff', '#00f7ff', '#00fff2']),  # very light blue
        ('hydro_electric', ['#00004d', '#190099', '#0d0099',
                            '#000099', '#000d99', '#001a99', '#002699']),  # dark blue
        ('combined_heat_power', ['#6b248f', '#7a29a3', '#8a2eb8', '#9933cc',
                                 '#a347d1', '#ad5cd6', '#b870db']),  # violet
        ('power_plant', ['#b34700', '#cc5200', '#c65c00', '#ff6600',
                         '#ff751a', '#ff8533', '#ff944d']),  # pure orange
        ('heat_plant', ['#670000', '#800000', '#9a0000', '#b30000',
                        '#cd0000', '#e60000', '#ff0000']),  # strong red
        ('electrical_line', ['#b38f00', '#cca300', '#e6b800', '#ffcc00',
                             '#ffd11a', '#ffd633', '#ffdb4d']),  # pure yellow
        ('gas_pipeline', ['#1a3333', '#224444', '#2b5555', '#336666',
                          '#3c7777', '#448888', '#4d9999']),  # v. dark d. cyan
        ('gas_delivery', ['#003434', '#004d4d', '#006767', '#008080',
                          '#009a9a', '#00b3b3', '#00cdcd']),  # very dark cyan
        ('oil_pipeline', ['#404040', '#4d4d4d', '#595959', '#666666',
                          '#737373', '#808080', '#8c8c8c']),  # very dark grey
        ('oil_delivery', ['#0d0d0d', '#1a1a1a', '#262626', '#333333',
                          '#404040', '#4d4d4d', '#595959']),  # darker grey
        ('hydro_electrical_storage', ['#000080', '#000099', '#0000b3',
                                      '#0000cc', '#0000c6',
                                      '#0000ff', '#1a1aff']),  # strong blue
        ('electro_chemical_storage', ['#8fb300', '#a3cc00', '#b8e600',
                                      '#ccff00', '#d1ff1a', '#d6ff33',
                                      '#dbff4d']),  # pure yellow
        ('electro_mechanical_storage', ['#343400', '#4d4d00', '#676700',
                                        '#808000', '#9a9a00', '#b3b300',
                                        '#cdcd00']),  # dark yellow
        ('thermal_energy_storage', ['#800020', '#990026', '#b3002a',
                                    '#cc0033', '#e60039', '#ff0040',
                                    '#ff1a53']),  # strong red
        ('power2x', ['#476b6b', '#527a7a', '#5c8a8a', '#669999',
                     '#75a3a3', '#85adad', '#94b8b8']),  # desaturat. dark cyan
        ('power2heat', ['#670000', '#800000', '#9a0000', '#b30000',
                        '#cd0000', '#e60000', '#ff0000']),  # strong red
        ('imported', ['#b33500', '#cc3d00', '#e64400', '#ff4c00',
                      '#ff5e1a', '#ff7033', '#ff824d']),  # orange
        ('backup', ['#340034', '#4d004d', '#670067', '#800080',
                    '#9a009a', '#b300b3', '#cd00cd']),  # dark magenta
        ('demand', ['#1a004d', '#220066', '#2b0080', '#330099',
                    '#3b00b3', '#4400cc', '#4c00e6']),  # dark violet
        ('export', ['#001800', '#003100', '#004b00', '#006400',
                    '#007e00', '#009700', '#00b100']),  # dark green
        ('excess', ['#800000', '#990000', '#b30000', '#cc0000',
                    '#e60000', '#ff0000', '#ff1a1a']),  # pure red
    ]),
)
""" Tessif colormap themes. Stored inside a
:attr:`~tessif.frused.namedtuples.NodeColorGroupings`
:class:`~typing.NamedTuple`. Assembled using `colorhexa
<https://www.colorhexa.com/>`_
Categorized by :attr:`~tessif.frused.namedtuples.NodeColorGroupings`

For each category there is a mapping of identifiers to colors

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    import tessif.frused.themes as themes
    import pandas

    for pos, dct in enumerate(themes.cmaps):
        category = themes.cmaps._fields[pos]

        path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_colormaps.png'.format(category))
        fig = themes._plot_color_gradients(category, dct)
        fig.savefig(path)

        csv_path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_colormaps.csv'.format(category))

        df = pandas.DataFrame(data=dct.values(),
                              index=dct.keys())

        df.to_csv(csv_path, header=None)

|

**Component Grouped Colormaps:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/component_colormaps.csv

.. image:: themes/component_colormaps.png
    :align: center
    :alt: Image showing the supported component colormaps

|

**Name Grouped Colormaps:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/name_colormaps.csv
    :stub-columns: 1

.. image:: themes/name_colormaps.png
    :align: center
    :alt: Image showing the supported name colormaps

|

**Carrier Grouped Colormaps:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/carrier_colormaps.csv
    :stub-columns: 1

.. image:: themes/carrier_colormaps.png
    :align: center
    :alt: Image showing the supported carrier colormaps

|

**Sector Grouped Colormaps:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/sector_colormaps.csv
    :stub-columns: 1

.. image:: themes/sector_colormaps.png
    :align: center
    :alt: Image showing the supported sector colormap
"""

ccycles = NodeColorGroupings(*[
    collections.OrderedDict([
        (catgry, cycle(color_list))
        for catgry, color_list in cmaps._asdict()[key].items()])
    for key in cmaps._asdict().keys()])
"""
:mod:`~tessif` cycled colormaps. Stored inside a
:attr:`~tessif.frused.namedtuples.NodeColorGroupings`
:class:`~typing.NamedTuple`.
"""

hatches = NodeColorGroupings(
    component=collections.OrderedDict([
        ('bus', '/'),
        ('sink', '\\'),
        ('source', '.'),
        ('storage', '|'),
        ('transformer', '-'),
        ('connector', 'x'),
    ]),
    carrier=collections.OrderedDict([
        ('solar', '/'),
        ('wind', '\\'),
        ('water', '.'),
        ('biomass', '|'),
        ('gas', '-'),
        ('oil', '+/'),
        ('lignite', 'o'),
        ('hardcoal', '.'),
        ('nuclear', '*'),
        ('electricity', '//'),
        ('steam', '\\\\'),
        ('hot_water', '||'),
    ]),
    sector=collections.OrderedDict([
        ('power', '/'),
        ('heat', '\\'),
        ('mobility', '|'),
        ('coupled', 'x'),
    ]),
    name=collections.OrderedDict([
        ('photovoltaic', '/'),
        ('solarthermal', '//'),
        ('onshore', '\\'),
        ('offshore', '\\\\'),
        ('hydro_electric', 'o'),
        ('combined_heat_power', '+'),
        ('power_plant', '|'),
        ('heat_plant', '-'),
        ('electrical_line', '++'),
        ('gas_pipeline', '--'),
        ('gas_delivery', '---'),
        ('oil_pipeline', '+/'),
        ('oil_delivery', '+/+/'),
        ('bus', '.'),
        ('hydro_electrical_storage', 'oo'),
        ('electro_chemical_storage', 'xx'),
        ('electro_mechanical_storage', '||'),
        ('thermal_energy_storage', '--'),
        ('power2x', 'xxx'),
    ]),
)
"""
:mod:`~tessif` hatch themes. Stored inside a
:attr:`~tessif.frused.namedtuples.NodeColorGroupings`
:class:`~typing.NamedTuple`.

For each category there is a mapping of identifiers to hatches

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    import tessif.frused.themes as themes
    import pandas
    import dutils

    for pos, dct in enumerate(themes.hatches):
        category = themes.hatches._fields[pos]

        path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_hatches.png'.format(category))
        fig = themes._plot_hatches(category, dct)
        fig.savefig(path)

        csv_path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_hatches.csv'.format(category))

        for key, value in dct.copy().items():
            dct[key] = '{lit_quote}{value}{lit_quote}'.format(
                lit_quote='``', value=value)

        df = dutils.to_dataframe(dct, columns=2, fillvalue='')

        df.to_csv(csv_path, header=None)

|

**Component Grouped Hatches:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/component_hatches.csv
    :stub-columns: 1

.. image:: themes/component_hatches.png
    :align: center
    :alt: Image showing the supported name hatches

|

**Name Grouped Hatches:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/name_hatches.csv
    :stub-columns: 1

.. image:: themes/name_hatches.png
    :align: center
    :alt: Image showing the supported name hatches

|

**Carrier Grouped Hatches:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/carrier_hatches.csv
    :stub-columns: 1

.. image:: themes/carrier_hatches.png
    :align: center
    :alt: Image showing the supported carrier hatches

|

**Sector Grouped Hatches:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/sector_hatches.csv
    :stub-columns: 1

.. image:: themes/sector_hatches.png
    :align: center
    :alt: Image showing the supported sector hatches
"""


hmaps = {
    'sector': collections.OrderedDict([
        ('power', ['/', '\\', '//', '\\\\', '///', '\\\\\\']),
        ('heat', ['-', '|', '--', '||', '---', '|||']),
        ('mobility', ['x', '+/', 'xx', '+/+/', 'xxx', '+/+/+/']),
    ]),
}
"""
Mapping of :mod:`~tessif` hatchmaps. Usefull when plotting sector grouped
results to distinguish the individual components without coloring.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    import tessif.frused.themes as themes
    import pandas
    import dutils

    for category, dct in themes.hmaps.items():

        csv_path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'themes', '{}_hatchmaps.csv'.format(category))

        for key, value in dct.copy().items():
            new_list = []
            for i in value:
                new_list.append(
                    '{lit_quote}{i}{lit_quote}'.format(lit_quote='``', i=i))
            dct[key] = new_list

        df = pandas.DataFrame(data=dct.values(),
                              index=dct.keys())

        df.to_csv(csv_path, header=None)

|

**Sector Grouped Hatchmap:**

.. csv-table:: internal representation
    :file: source/api/frused/themes/sector_hatchmaps.csv
    :stub-columns: 1
"""


def _plot_colortable(colors, title, sort_colors=True, emptycols=0):
    """
    Utility for plotting color themes. Inspired by
    matplotlib's `documentation
    <https://matplotlib.org/3.2.2/gallery/color/named_colors.html>`_.
    """

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    topmargin = 40

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)

    n = len(names)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-topmargin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(title, fontsize=24, loc="left", pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        swatch_end_x = cell_width * col + swatch_width
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.hlines(y, swatch_start_x, swatch_end_x,
                  color=colors[name], linewidth=18)

    return fig


def _plot_color_gradients(category, cmap_dct):
    """
    Utility for plotting colormap examples. Inspired by
    matplotlib's `documentation
    <https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html>`_.
    """
    import numpy as np

    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    fig, axes = plt.subplots(nrows=len(cmap_dct))
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title(category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_dct):
        ax.imshow(gradient, aspect='auto',
                  cmap=mcolors.ListedColormap(cmap_dct[name]))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

    return fig


def _plot_hatches(category, hatch_map, sort_colors=True, emptycols=0):
    """
    Utility for plotting color themes. Inspired by
    matplotlib's `documentation
    <https://matplotlib.org/3.2.2/gallery/color/named_colors.html>`_.

    And a pach hatching example from `so
    <https://stackoverflow.com/a/25185432>`
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    topmargin = 40

    n = len(hatch_map)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-topmargin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(category, fontsize=24, loc="left", pad=10)

    for i, name in enumerate(hatch_map):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        swatch_end_x = cell_width * col + swatch_width
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(patches.Rectangle(
            (swatch_start_x, y-9), swatch_end_x-swatch_start_x, 18,
            hatch=hatch_map[name], fill=False, snap=False, linewidth=0))

    return fig


def match_theme(strings, theme='colors', grouping='name',):
    """
    Match a collection of strings to tessf's theme groupings

    Parameters
    ---------
    strings: ~collections.abc.Iterable
        Iterable of strings which are tried to be matched to registerd theme
        values.
    theme: str
        String specifying one of :mod:`tessif's themes <tessif.frused.themes>`
        like ``colors``, etc.
    grouping: str
        String specifying one of the
        :attr:`~tessif.frused.namedtuples.NodeColorGroupings` the
        :paramref:`~match_theme.theme` provides

    Return
    ------
    dict
        Mapping of the provided strings to the matched theme values

    Example
    -------
    Create a :class:`tessif energy system
    <tessif.model.energy_system.AbstractEnergySystem>` and create a color
    mapping using it's nodes:

    1. Create the tessif energy system using the :ref:`Example Hub <Examples>`:

       >>> import tessif.examples.data.tsf.py_hard as coded_examples
       >>> tessif_es = coded_examples.create_fpwe()

    2. Create a list of node names:
       >>> node_names = [str(node.uid) for node in tessif_es.nodes]

    3. Match the node colors:

       >>> from tessif.frused.themes import match_theme
       >>> node_colors = match_theme(
       ...     strings=node_names, theme='colors', grouping='name')

       >>> import pprint
       >>> pprint.pprint(node_colors)
       {'Battery': '#ccff00',
        'Demand': '#330099',
        'Gas Station': '#6633cc',
        'Generator': '#ff6600',
        'Pipeline': '#336666',
        'Powerline': '#ffcc00',
        'Solar Panel': '#ff9900'}
    """
    matched_theme = dict()
    for string in strings:

        # get requested theme group of this module
        theme_group = getattr(globals().get(theme), grouping)

        # reconstruct the uid from its string representation:
        uid = Uid.reconstruct(string)

        # match reconstructed uid groupings attribute to spellings:
        for registered_key in theme_group:
            if any(tag == getattr(uid, grouping) for tag in getattr(
                    spellings, registered_key)):
                matched_theme[string] = theme_group[registered_key]

    return matched_theme
