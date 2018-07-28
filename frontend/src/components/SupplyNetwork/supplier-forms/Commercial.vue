<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='120px')
    el-form-item(label='Lead time')
      el-input-number(size='small', v-model='form.lead_time')
    el-form-item(label='Cost / bp')
      el-input-number(size='small', v-model='form.cost')

</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
