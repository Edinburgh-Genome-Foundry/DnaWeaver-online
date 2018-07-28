<template lang='pug'>

.node(:style="nodeStyle")
  el-popover(ref='chooseParents', placement='bottom', width='400px', trigger='click')
    .parents-form
      h4 Create a new supplier
      span.button-span.create-suppliers-button(v-for='data, type in suppliersInfos', :key='type',
                       v-if="nodeInfos.suppliers.indexOf(type) > -1")
        el-tooltip(class="item" effect="light", :content="data.defaultLabel" placement="top")
          el-button(@click="$emit('newConnectingNode', {type, connectsTo: nodeData.id})" circle)
            font-awesome-icon(:icon='data.icon')
      div(style="display: block;height: 20px")
      h4 Or select existing suppliers
      el-select(v-model='nodeData.parents' multiple, placeholder='Select suppliers')
        el-option(v-for='node in nodes', :key='node.id', :value='node.id', :label='node.label'
                  v-if='notAChild[node.id]')
  el-popover(ref='chooseParams', placement='bottom', width='350', trigger='click')
    .form(:is="formComponent", v-model='nodeData.params')

  font-awesome-icon.icon(:icon='nodeInfos.icon')
  input.label(v-if='options.showLabels' v-model='nodeData.label', :style='{color: nodeInfos.color}')
  .toolbar(v-if='options.showToolbar')
    el-button-group
      el-tooltip(class="item" effect="light", content="delete", placement="bottom")
        el-button(
                  v-if='nodeInfos.isDeletable',
                  @click="$emit('delete')"
                  icon='el-icon-delete'
                  c)
      el-tooltip(class="item" effect="light", content='suppliers', placement="bottom")
        <el-button v-if='nodeInfos.acceptsParents' icon='el-icon-share' v-popover:chooseParents>
        </el-button>
      el-tooltip(class="item" effect="light", content='options', placement="bottom")
        <el-button size='tiny' v-if='nodeInfos.hasParams' v-popover:chooseParams title='options'>
          <font-awesome-icon icon='list'/>
        </el-button>
</template>

<script>

const suppliersInfos = require('./json/suppliers.json')
const suppliersForms = {
  'commercial': require('./supplier-forms/Commercial.vue').default,
  'main': require('./supplier-forms/Main.vue').default,
  'assembly': require('./supplier-forms/Assembly.vue').default,
  'pcr': require('./supplier-forms/PCR.vue').default
}

export default {
  props: {
    value: {default: null},
    nodes: {default: () => ([])},
    options: {default: () => ({})}
  },
  data () {
    console.log('PARAAAAMS', this.value.params)
    return {
      nodeData: this.value,
      nodeInfos: Object.assign({}, suppliersInfos.default, suppliersInfos[this.value.type]),
      suppliersInfos: suppliersInfos,
      formComponent: suppliersForms[this.value.type]
    }
  },
  watch: {
    nodeData: {
      deep: true,
      handler (v) {
        this.$emit('input', v)
      }
    }
  },
  computed: {
    notAChild () {
      var result = {}
      var children = {}
      Object.keys(this.nodes).forEach(function (nid) {
        result[nid] = true
        children[nid] = []
      })
      for (var nid in this.nodes) {
        for (var parentid of this.nodes[nid].parents) {
          children[parentid].push(nid)
        }
      }
      function rec (nid) {
        result[nid] = false
        for (var newId of children[nid]) {
          rec(newId)
        }
      }
      rec(this.nodeData.id)
      return result
    },
    nodeStyle () {
      return {
        width: this.options.size.width + 'px',
        height: (this.options.size.height) + 'px',
        color: this.nodeInfos.color,
        'padding-top': (this.options.showToolbar ? 1 : 0.5) + 'em'
      }
    }
  },
  contentType: 'html'
}
</script>
<style lang='scss' scoped>

hr.pencil {
    border: 0;
    height: 1px;
    background: #333;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    background-image: linear-gradient(to right, #ccc, #333, #ccc);
}
.pop {
  background-color: blue;
}
.node {
  display: inline-block;
  font-size: 0.9em;
  padding-top: 0.5em;

  .icon {
    display: inline-block;
    width: auto;
    // margin-top: 5px;
    height: 24px;
    margin-bottom: 0;
  }
  .label {
    margin-top: 0;
    margin-left: auto;
    text-align: center;
    max-width: 100%;
    border: none !important;
    outline: 0 !important;
    border-color: Transparent;
    font-size: 1em;
    resize: none;
  }

  .toolbar {
    display: block;
    background-color: white;
    // visibility: hidden;
    margin-top: 2%;
    margin-bottom: 5%;
    .el-button {
      padding: 0.2em;

      // margin: 0.1em;
      // width: 2em;
      font-size: 1em;
      // border: 0px;
    }
  }
  &:hover /deep/ {
    .toolbar {
      visibility: visible;
    }
  }
}
</style>

<style lang='scss'>

.parents-form {
  font-family: 'Open Sans';
  text-align: center !important;
  h4 {
    margin-top: 0.3em;
    margin-bottom: 1em;
  }
  text-align: left;
  width: 100%;
  // .el-button {
  //   padding: 0.3em;
  //   margin-right: 0.5em;
  //   font-size: 1.5em;
  // }
  /deep/ input {
    font-size: 0.8em !important;
    width: 400px;
  }
  .create-suppliers-button button {
    font-size: 1em;
    border: 0 !important;
  }
}

</style>
