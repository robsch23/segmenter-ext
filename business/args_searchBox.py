from loko_extensions.model.components import Arg

range_box_height_searchBox = Arg(name='range_box_height',
                                 group='Search Box',
                                 type="text",
                                 label='Range of boxes height sizes',
                                 helper="Sets the minimum and maximum height of the boxes that must be returned in output (set 0 for any measurement)",
                                 value='0,0',
                                 description="Sets the minimum and maximum height of the boxes that must be returned in output"
                                 )
range_box_width_searchBox = Arg(name='range_box_width',
                                group='Search Box',
                                type="text",
                                label='Range of boxes width sizes',
                                helper="Sets the minimum and maximum width of the boxes that must be returned in output (set 0 for any measurement)",
                                value='0,0',
                                description="Sets the minimum and maximum width of the boxes that must be returned in output"
                                )

range_box_area_searchBox = Arg(name='range_box_area',
                               group='Search Box',
                               type="text",
                               label='Range of boxes area sizes',
                               helper="Sets the minimum and maximum area of the boxes that must be returned in output (set 0 for any measurement)",
                               value='0,0',
                               description="Sets the minimum and maximum area of the boxes that must be returned in output"
                               )
