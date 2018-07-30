<template lang='pug'>
el-row
  el-row(:gutter='0')
    el-col(:span='3'): center: .slider-data {{valueMirror[0]}}
    el-col(:span='17')
      el-slider(size='small', v-model='valueMirror', :step="step", range,
                :min='min', :max='max', :disabled='disabled')
    el-col(:span='3'): center: .slider-data {{valueMirror[1]}}
</template>
<script>
export default {
  props: {
    value: {default: () => ([0, 10])},
    min: {default: 0},
    max: {default: 10},
    step: {default: 1},
    disabled: {default: false}
  },
  data () {
    return {
      valueMirror: this.value
    }
  },
  watch: {
    value: {
      deep: true,
      handler (val) {
        this.valueMirror = val
      }
    },
    valueMirror: {
      deep: true,
      handler (val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>

<style lang='scss' scoped>
.slider-data {
  font-size: 0.8em;
}
</style>
