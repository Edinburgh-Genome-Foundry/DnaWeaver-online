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
      el-input-number(size='small', v-model='form.pcr_homology_length')
    el-form-item(label='Max overhang size')
      el-input-number(size='small', v-model='form.max_overhang_length')
</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
