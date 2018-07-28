<script>
export default {
  props: {
    value: {default: {}}
  },
  data () {
    return {
      form: this.value
    }
  },
  watch: {
    form: {
      deep: true,
      handler (val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>
