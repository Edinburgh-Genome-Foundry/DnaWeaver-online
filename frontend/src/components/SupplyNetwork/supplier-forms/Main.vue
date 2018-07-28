<template lang='pug'>
.supplier-form
  //- el-form(ref="form", label-width='120px')
  //-   //- el-form-item(label='Sequence')
  //-   //-   sequence-uploader(v-model='form.sequence')
  //-   el-form-item(label='Optimization')
  //-     el-select(v-model='form.optimization')
  //-       el-option(value='cheapest', label='Cheapest plan')
  //-       el-option(value='cheapest_with_deadline', label='Cheapest with deadline')
  //-       el-option(value='fastest_under_budget', label='Fastest under budget')
  //-   el-form-item(v-if="form.optimization == 'cheapest_with_deadline'" label='Deadline')
  //-     el-input-number(size='small' v-model='form.deadline')
  //-   el-form-item(v-if="form.optimization == 'fastest_under_budget'" label='Deadline')
  //-     el-input-number(size='small' v-model='form.budget')
  //- backend-querier
</template>

<script>
import NodeForm from './NodeForm.vue'
export default {
  extends: NodeForm
}
</script>
