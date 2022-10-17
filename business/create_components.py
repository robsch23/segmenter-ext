"""
File utile per creare il file components.json nella directory extensions
"""
from loko_extensions.model.components import Arg, save_extensions, Component, Input, Output
from business.args_searchBox import range_box_height_searchBox, range_box_area_searchBox, range_box_width_searchBox
from business.args_segment import dpi_segment, range_kernel_size_segment, dilate_iteration_segment, \
    range_blocks_height_segment, range_blocks_width_segment, range_blocks_area_segment

# general args
save_images = Arg(name='save_images',
                  type="boolean",
                  label='Save Images',
                  )

segmenter = Component(name="Segmenter",
                      args=[save_images, dpi_segment, range_kernel_size_segment, dilate_iteration_segment,
                            range_blocks_height_segment, range_blocks_width_segment,
                            range_blocks_area_segment, range_box_width_searchBox, range_box_height_searchBox,
                            range_box_area_searchBox
                            ],
                      inputs=[
                          Input(id='Segment',
                                service='loko/segmenter/segment',
                                to='Segment'),
                          Input(id='Search Box',
                                service='loko/segmenter/search_box',
                                to='Search Box')
                      ],
                      outputs=[
                          Output(id='Segment'),
                          Output(id='Search Box')
                      ])

save_extensions([segmenter])
