<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='150px')
    el-form-item(label='Collection')
      el-select(v-model='form.collection')
        el-option(label='EMMA' value='EMMA')
    el-form-item(label='Duration (days)')
      el-input-number(size='small', v-model='form.duration')
    el-form-item(label='Cost / part ($)')
      el-input-number(size='small', v-model='form.cost', :step='0.05',
                      :min='0', :max='1000.0')

</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
