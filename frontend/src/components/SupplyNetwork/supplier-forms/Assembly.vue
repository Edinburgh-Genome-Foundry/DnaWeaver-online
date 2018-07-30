<template lang='pug'>
.supplier-form
  h3(align='center') Assembly Parameters
  el-form(ref="form", label-width='160px')
    el-form-item(label='Cost ($)')
      el-input-number(size='small', v-model='form.cost')
    el-form-item(label='Duration (days)')
      el-input-number(size='small', v-model='form.duration')
    el-form-item(label='Method')
      el-select(v-model='form.method')
        el-option(value='yeast_recombination', label='Yeast recombination')
        el-option(value='gibson_assembly', label='Gibson Assembly')
        el-option(value='type_iis', label='Type IIS (Golden Gate)')
        el-option(value='oligo_assembly', label='Oligo assembly')
    el-form-item(label='Overhang design' v-if="form.method !== 'type_iis'")
      el-select(v-model='form.overhang_type')
        el-option(value='fixed_size', label='Fixed size')
        el-option(value='tm', label='Target Tm')

    el-form-item(label='Tm (C)' v-if="(form.overhang_type == 'tm') && (form.method !== 'type_iis')")
      detail-slider(v-model='form.tm_range', :min='20', :max='120' range)
    el-form-item(label='Overhang size (bp)' v-if="(form.overhang_type == 'tm') && (form.method !== 'type_iis')")
      detail-slider(v-model='form.overhang_size_range', :min='10', :max='120' range)

    el-form-item(
      label='Overlap (bp)'
      v-if="(form.overhang_type == 'fixed_size') && (form.overhang_type == 'fixed_size')"
      )
      el-input-number(v-model='form.overlap', :min='10', :max='20000', size='small')
    el-form-item(label='Enzyme' v-if="form.method === 'type_iis'")
      el-select(v-model='form.enzyme')
        el-option(value='BsmBI', label='BsmBI')
        el-option(value='BsaI', label='BsaI')
        el-option(value='BbsI', label='BbsI')
    el-form-item(label='Limit Construct Size')
      el-checkbox(v-model='form.use_size_range')
    el-form-item(v-if='form.use_size_range' label='Construct Size (bp)')
      detail-slider(v-model='form.size_range', :step="5", :min='10', :max='50000')
    el-form-item(label='Max Fragments' v-if='!form.use_astar')
      el-input-number(size='small', v-model='form.max_fragments', :min='2', :max='100')
    el-form-item(label='Fragments size')
      detail-slider(v-model='form.fragments_size_range', :min='20', :max='30000', :step='5')

  hr(style='margin-top: 1em; margin-bottom: 1em;')
  h3(align='center') Solver Parameters
  el-form(label-width='160px')
    el-form-item(label='Grain')
      el-select(v-model='form.grain_type')
        el-option(value='auto', label='Auto')
        el-option(value='manual', label='Manual')
    el-form-item(label='First Pass Grain' v-if="form.grain_type === 'manual'")
      el-input-number(v-model='form.coarse_grain', :min='1', :max='20000', size='small')
    el-form-item(label='Refinement Grain' v-if="form.grain_type === 'manual'")
      el-input-number(v-model='form.fine_grain', :min='0', :max='form.coarse_grain', size='small')
    el-form-item(label='Use A*')
      el-checkbox(v-model='form.use_astar')

</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
