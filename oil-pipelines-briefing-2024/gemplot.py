import matplotlib.pyplot as mp
import matplotlib
import numpy
import textwrap

# set open sans as default font
mp.rcParams['font.family'] = 'Open Sans'

################################################################################
# GEMPLOT VARIABLES
################################################################################

base_ratio = 1.0
base_size = base_ratio*12 # 1 rem is 12pt font

color_title_text = '#222222'
color_subtitle_text = '#525252'
color_axis_text = '#525252'
color_legend_text = '#525252'
color_footnote_text = '#525252'
color_source_text = '#525252'
color_gridlines = '#cbcbcb'

# 1 pixel is 0.75 points
title_subtitle_spacing = 18/0.75 # pt divided by .75 to convert to pixel (1.5rem)
subtitle_plot_spacing = 12/0.75 # pt divided by .75 to convert to pixel (1rem)
margin = 0.5/0.75 # pt divided by .75 to convert to pixel

thickness_gridlines = 0.5/0.75 # 0.5 pt, convert to px
thickness_emphasize_axis = 1.5

font_size_legend = 1.3331*base_size
font_size_subtitle = 1.53*base_size
font_size_title = 2*base_size
font_size_footnote = 1.1669*base_size
font_size_axis = 1.3331*base_size
font_size_source = 1*base_size

line_height_title = 1.35
line_height_subtitle = 1.45
line_height_footnote = 1.2

text_weight_normal = 400
text_weight_bold = 700

width_pixels = 640 # default
height_pixels = 450 # default

################################################################################
# GEMPLOT FUNCTIONS
################################################################################
def gemplot_note(ax=None,
                   fig=None,
                   note_text=None,
                   note_position=0,
                   multiple_axes=False):
    """
    needs ax, fig, note_text to be specified
    text_ratio: decrease to make footer text smaller
    footer_position: default 1, INCREASE to 1.25, 1.5, etc. to move the logo and text DOWN

    if it's a complex, multi-axis figure, specify that with multiple_axes=True
    """
    if not ax or not note_text or not fig:
        print('!!! FOOTER NOT ADDED: add_gem_footer() requires an axis (ax=), a figure (fig=), and text (text=)')
        return

    if not multiple_axes:
        ax_bbox = ax.get_tightbbox(renderer=fig.canvas.renderer)
        x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0,ax_bbox.y0])

        ax.text(s=note_text,
                size=font_size_footnote,
                color=color_footnote_text,
                x=x_loc,
                y=y_loc-note_position,
                ha='left',
                va='top',
                weight=text_weight_normal,
                transform=ax.transAxes,
                linespacing=line_height_footnote,
                wrap=False)

def gemplot_footer(ax=None,
                   fig=None,
                   footer_text=None,
                   footer_position=1.0,
                   multiple_axes=False):
    """
    needs ax, fig, footer_text to be specified
    text_ratio: decrease to make footer text smaller
    footer_position: default 1, INCREASE to 1.25, 1.5, etc. to move the logo and text DOWN

    if it's a complex, multi-axis figure, specify that with multiple_axes=True
    """
    if not ax or not footer_text or not fig:
        print('!!! FOOTER NOT ADDED: add_gem_footer() requires an axis (ax=), a figure (fig=), and text (text=)')
        return
    
    gem_logo = matplotlib.image.imread('/Users/baird/Dropbox/_git_ALL/_github-repos-gem/gemplot-python/data/gem_logo_padding.png')
    logo_image_box = matplotlib.offsetbox.OffsetImage(gem_logo, zoom=0.035)

    if not multiple_axes:
        # import GEM logo
        logo_annotation_box = matplotlib.offsetbox.AnnotationBbox(logo_image_box,
                                                                  (1,0), # sets box alignment to lower right corner
                                                                  xycoords='axes fraction',
                                                                  box_alignment=(1.,1.5*footer_position), 
                                                                  frameon=False,
                                                                  )

        ax.add_artist(logo_annotation_box)
        gem_logo_bbox = logo_annotation_box.get_tightbbox(renderer=fig.canvas.renderer)
        ax_bbox = ax.get_tightbbox(renderer=fig.canvas.renderer)

        x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0,ax_bbox.y0])
        logo_x0_loc,logo_y0_loc = ax.transAxes.inverted().transform([gem_logo_bbox.x0,gem_logo_bbox.y0])
        logo_x1_loc,logo_y1_loc = ax.transAxes.inverted().transform([gem_logo_bbox.x1,gem_logo_bbox.y1])

        ax.text(s=footer_text,
                size=font_size_footnote,
                color=color_footnote_text,
                x=x_loc,
                y=(logo_y0_loc+logo_y1_loc)/2,
                ha='left',
                va='center',
                weight=text_weight_normal,
                transform=ax.transAxes,
                linespacing=line_height_footnote,
                wrap=False)
    
    if multiple_axes:
        # ax_list = fig.axes
        # ax_bbox_list = []
        # for ax in ax_list:
        #     ax_bbox_list.append(ax.get_tightbbox())
        # left_extremity = ax_bbox_list[0].y0
        # right_extremity = ax_bbox_list[0]
        # bottom_extremity = ax_bbox_list[0]
        # top_extremity = ax_bbox_list[0]
        # for ax_bbox in ax_bbox_list[1:]:
        #     if ax_bbox.y0 < left_extremity:



        # get right-most object
        # get left-most object
        # get top object
        # get bottom object
        return

def gemplot_title_subtitle(ax=None,
                       legend=None,
                       fig=None,
                       title_text=None,
                       subtitle_text=None,
                       vertical_shift=0.05,
                       multiple_axes=False):
    """
    needs ax, fig, title_text subtitle_text to be specified
    text_ratio: decrease to make footer text smaller
    footer_position: default 1, INCREASE to 1.25, 1.5, etc. to move the logo and text DOWN
    """
    if not multiple_axes:
        if not ax or not title_text or not subtitle_text:
            print('!!! FOOTER NOT ADDED: add_title_subtitle(multiple_axes=False) requires an axis (ax=), title_text (title_text=), and subtitle_text (subtitle_text)')
            return
            
        if legend:
            # if there's a legend, you base placement on that
            ax_bbox = legend.get_tightbbox(renderer=fig.canvas.renderer)
            x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0, ax_bbox.y1])
        else:
            ax_bbox = ax.get_tightbbox(renderer=fig.canvas.renderer)
            x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0, ax_bbox.y1])

        ax.text(s=subtitle_text,
                size=font_size_subtitle,
                color=color_subtitle_text,
                x=x_loc,
                y=y_loc+vertical_shift,
                ha='left',
                va='bottom',
                weight=text_weight_normal,
                transform=ax.transAxes,
                linespacing=line_height_title,
                wrap=False)
    
    if multiple_axes:
        if not fig or not title_text or not subtitle_text:
            print('!!! FOOTER NOT ADDED: add_title_subtitle(multiple_axes=True) requires a figure (fig=), title_text (title_text=), and subtitle_text (subtitle_text)')
            return
            
        if legend:
            # if there's a legend, you base placement on that
            ax_bbox = legend.get_tightbbox()
            x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0, ax_bbox.y1])
        else:
            ax_bbox = ax.get_tightbbox()
            x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0, ax_bbox.y1])

        ax.text(s=subtitle_text,
                size=font_size_subtitle,
                color=color_subtitle_text,
                x=x_loc,
                y=y_loc+vertical_shift,
                ha='left',
                va='bottom',
                weight=text_weight_normal,
                transform=ax.transAxes,
                linespacing=line_height_title,
                wrap=False)
    
    ax_bbox = ax.get_tightbbox(renderer=fig.canvas.renderer)
    x_loc,y_loc = ax.transAxes.inverted().transform([ax_bbox.x0, ax_bbox.y1])
    ax.text(s=title_text,
            size=font_size_title,
            color=color_title_text,
            x=x_loc,
            y=y_loc+vertical_shift,
            ha='left',
            va='bottom',
            weight=text_weight_bold,
            transform=ax.transAxes,
            linespacing=line_height_subtitle,
            wrap=False)

def gemplot_axes(ax=None, fig=None):
    if not ax or not fig:
        print('NEED AN AXIS')
        return

    # update gridlines
    # update axis sizes
    ax.tick_params(size=0, 
                   labelsize=font_size_axis,
                   colors=color_axis_text)
    
    ax.set_xlabel(ax.xaxis.get_label_text(),
                  size=font_size_axis,
                  color=color_axis_text)
    
    ax.set_ylabel(ax.yaxis.get_label_text(),
                  size=font_size_axis,
                  color=color_axis_text)

def gemplot_grid(ax=None, fig=None, which='major', xyaxis='x'):
    ax.set_axisbelow(True)
    if which=='major':
        ax.grid(which='major', 
                axis=xyaxis,
                lw=thickness_gridlines,
                color=color_gridlines)
    if which=='minor':
        ax.grid(which='major', 
                axis=xyaxis,
                lw=thickness_gridlines,
                color=color_gridlines)
    if which=='both':
        ax.grid(which='both', 
                axis=xyaxis,
                lw=thickness_gridlines,
                color=color_gridlines)

def gemplot_left_axis(ax=None, fig=None):
    ax.spines[['right','top','bottom']].set_visible(False)
    ax.spines['left'].set_color(color_axis_text)
    ax.spines['left'].set_linewidth(thickness_emphasize_axis)