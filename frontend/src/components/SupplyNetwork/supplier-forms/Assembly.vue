<template lang='pug'>
.supplier-form
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
    el-form-item(label='Overhang design')
      el-select(v-model='form.overhang_type')
        el-option(value='fixed_size', label='Fixed size')
        el-option(value='tm', label='Target Tm')

    el-form-item(label='Tm (C)' v-if="(form.overhang_type == 'tm')")
      detail-slider(v-model='form.tm_range', :min='20', :max='120' range)
    el-form-item(label='Overhang size (bp)' v-if="(form.overhang_type == 'tm')")
      detail-slider(v-model='form.overhang_size_range', :min='10', :max='120' range)

    el-form-item(
      label='Overlap (bp)'
      v-if="(form.overhang_type == 'fixed_size') && form.overhang_type == 'fixed_size'"
      )
      el-input-number(v-model='form.overlap', :min='10', :max='20000')
    el-form-item(label='Enzyme' v-if="form.method === 'type_iis'")
      el-select(v-model='form.enzyme')
        el-option(value='BsmBI', label='BsmBI')
        el-option(value='BsaI', label='BsaI')
        el-option(value='BbsI', label='BbsI')
    el-form-item(label='Max Fragments')
      el-input-number(size='small', v-model='form.max_fragments', :min='2', :max='100')
    el-form-item(label='Fragments size')
      detail-slider(v-model='form.fragments_size_range', :min='20', :max='10000', :step='10')

</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
