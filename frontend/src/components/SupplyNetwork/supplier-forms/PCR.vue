<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='180px')
    el-form-item(label='Cost ($)')
      el-input-number(size='small', v-model='form.cost')
    el-form-item(label='Duration (days)')
      el-input-number(size='small', v-model='form.duration')
    el-form-item(label='DNA bank')
      el-select(size='small', v-model='form.dna_bank')
        el-option(value='e_coli' label='E. coli')
        el-option(value='s_cerevisiae' label='S. cerevisiae')
    el-form-item(label='Max amplicon size (bp)')
      el-input-number(size='small', v-model='form.max_amplicon_length')
    el-form-item(label='Primer homology')
      el-select(v-model='form.homology_type')
        el-option(value='fixed_size', label='Fixed size')
        el-option(value='tm', label='Target Tm')
    el-form-item(label='Tm (C)' v-if="(form.homology_type == 'tm')")
      detail-slider(v-model='form.homology_size_range', :min='10', :max='120' range)
      detail-slider(v-model='form.tm_range', :min='20', :max='120' range)
    el-form-item(label='Homology size (bp)' v-if="form.homology_type == 'fixed_size'")
      el-input-number(size='small', v-model='form.homology_size')
    el-form-item(label='Max overhang size')
      el-input-number(size='small', v-model='form.max_overhang_length')
</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
