<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='120px')
    el-form-item(label='Method')
      el-select(v-model='form.method')
        el-option(value='yeast_recombination') Yeast recombination
        el-option(value='gibson_assembly') Gibson Assembly
        el-option(value='golden_gate') Type IIS (Golden Gate)
        el-option(value='oligo_assembly') Oligo assembly
    el-form-item(label='Cost')
      el-input-number(size='small', v-model='form.cost')
    el-form-item(label='Duration')
      el-input-number(size='small', v-model='form.duration')
</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
