<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='120px')
    el-form-item(label='Duration (days)')
      el-input-number(size='small', v-model='form.duration')
    el-form-item(label='Cost ($)')
      el-input-number(size='small', v-model='form.cost')
    el-form-item(label='DNA bank')
      el-select(size='small', v-model='form.dna_bank')
        el-option(value='e_coli' label='E. coli')
        el-option(value='s_cerevisiae' label='S. cerevisiae')
</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
