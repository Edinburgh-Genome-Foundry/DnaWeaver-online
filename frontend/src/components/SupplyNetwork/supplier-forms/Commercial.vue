<template lang='pug'>
.supplier-form
  el-form(ref="form", label-width='150px')
    el-form-item(label='Lead time (days)')
      el-input-number(size='small', v-model='form.lead_time')
    el-form-item(label='Cost ($/bp)')
      el-input-number(size='small', v-model='form.cost_per_bp', :step='0.05',
                      :min='0.01', :max='2.0')
    el-form-item(label='Size range (bp)')
      detail-slider(v-model='form.size_range', :step="5", :min='10', :max='7000')
    el-form-item(label='Valid GC%')
      detail-slider(v-model='form.gc_range', :step="1", :min='0', :max='100')
    el-form-item(label='Forbidden patterns')
      el-input(size='small', v-model='form.forbidden', type="textarea")

</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
