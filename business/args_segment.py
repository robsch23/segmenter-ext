from loko_extensions.model.components import Arg

dpi_segment = Arg(name="dpi",
                  group="Segment",
                  type="number",
                  label="DPI",
                  helper="Set dpi level --- Recommended range: 150-200",
                  value=200,
                  description='Set DPI level to decide on what level of scale to make the segmenter work --- Recommended range: 150-200')

range_kernel_size_segment = Arg(name='range_kernel_size',
                                group='Segment',
                                type="text",
                                label='Kernel Size Dilation',
                                helper="Set tuple of kernel for logic of dilation.  Example: 5,5 or 7,5 or 9,7...",
                                value="5,5",
                                description="The expansion width is set with the first element of the tuple. With the second element you set the height of the expansion"
                                )

dilate_iteration_segment = Arg(name='dilate_iteration',
                               group='Segment',
                               type="number",
                               label='Dilate iteration',
                               helper="Set number of iteration for dilate content in document",
                               value=10,
                               description="Set number of iteration for dilate content in document"
                               )

range_blocks_height_segment = Arg(name='range_blocks_height',
                                  group='Segment',
                                  type="text",
                                  label='Range of block height sizes',
                                  helper="Sets the minimum and maximum height of the blocks that must be returned in output (set 0 for any measurement)",
                                  value='0,0',
                                  description="Sets the minimum and maximum height of the blocks that must be returned in output"
                                  )
range_blocks_width_segment = Arg(name='range_blocks_width',
                                 group='Segment',
                                 type="text",
                                 label='Range of block width sizes',
                                 helper="Sets the minimum and maximum width of the blocks that must be returned in output (set 0 for any measurement)",
                                 value='0,0',
                                 description="Sets the minimum and maximum width of the blocks that must be returned in output"
                                 )

range_blocks_area_segment = Arg(name='range_blocks_area',
                                group='Segment',
                                type="text",
                                label='Range of block area sizes',
                                helper="Sets the minimum and maximum area of the blocks that must be returned in output (set 0 for any measurement)",
                                value='0,0',
                                description="Sets the minimum and maximum area of the blocks that must be returned in output"
                                )
