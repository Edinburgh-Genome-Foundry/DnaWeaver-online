<template lang='pug'>
.graph-editor
  svg(:width='layout.width', :height='layout.height', :viewBox='layout.viewBox')
    transition-group(name='path-elements',
                     enter-active-class='animated fadeIn slideInDown',
                     leave-active-class='animated fadeOut slideOutDown',
                     tag='g')
      g(v-for='edge in layout.edges', :key='edge.id')
        path.path(:d="pointsToPath(edge.points)")
    transition-group(name='svg-elements',
                     enter-active-class='animated fadeIn slideInDown',
                     leave-active-class='animated fadeOut slideOutDown',
                     tag='g')
      g.node-container(v-for='node in layout.nodes', :key='node.id')
        g(:transform="`translate(${node.x - 0.5*node.width}, ${node.y - 0.5 * node.height})`")
          foreignObject(:width='node.width', :height='node.height', overflow='visible')
            SupplierNode.component(v-model='nodes[node.id]',
                                  :nodes='nodes',
                                  :options='options.nodes',
                                  @newConnectingNode='newConnectingNode',
                                  @delete='deleteNode(node.id)')
</template>

<script>
import dagre from 'dagre'
import uuidv1 from 'uuid/v1'
import SupplierNode from './SupplierNode'

const suppliersInfos = require('./json/suppliers.json')

export default {
  props: {
    value: {default: () => ({})},
    graphDagreOptions: {default: () => ({})},
    options: {default: () => ({})}
  },
  data () {
    return {
      nodes: this.value,
      layout: {}
    }
  },
  methods: {
    updateLayout () {
      var g = new dagre.graphlib.Graph()
        .setGraph(this.options.dagre)
        .setDefaultEdgeLabel(function () { return {} })
      for (var nodeId in this.nodes) {
        var node = this.nodes[nodeId]
        g.setNode(nodeId, {
          width: this.options.nodes.size.width,
          height: this.options.nodes.size.height
        })
        for (var sourceId of node.suppliers) {
          g.setEdge(sourceId, nodeId)
        }
      }
      dagre.layout(g)
      var layout = {
        width: g.graph().width,
        height: g.graph().height + 20,
        nodes: [],
        edges: []
      }
      var self = this
      g.nodes().forEach(function (id) {
        var node = g.node(id)
        var nodeData = Object.assign({}, node, self.nodes[id])
        layout.nodes.push(nodeData)
      })
      var maxX = layout.width
      var minX = 0
      g.edges().forEach(function (e) {
        layout.edges.push({id: `${e.v}->${e.w}`, points: g.edge(e).points})
        for (var p of g.edge(e).points) {
          maxX = Math.max(maxX, p.x)
          minX = Math.min(minX, p.x)
        }
      })
      layout.viewBox = `${minX} 0 ${maxX - minX} ${layout.height}`
      layout.width = maxX - minX
      this.layout = layout
    },
    pointsToPath (points) {
      var list = [`M${points[0].x},${points[0].y}`]
      points.slice(1).map(function (p) { list.push(`L${p.x},${p.y}`) })
      return list.join('')
    },
    newConnectingNode (data) {
      var newId = uuidv1()
      this.nodes[data.connectsTo].suppliers.push(newId)
      this.$set(this.nodes, newId, {
        id: newId,
        name: suppliersInfos[data.type].defaultName,
        type: data.type,
        suppliers: [],
        parameters: JSON.parse(JSON.stringify(suppliersInfos[data.type].defaultParameters))
      })
    },
    deleteNode (nodeId) {
      var self = this
      Object.keys(this.nodes).map(function (nId) {
        self.nodes[nId].suppliers = self.nodes[nId].suppliers.filter((i) => (i !== nodeId))
      })
      this.$delete(this.nodes, nodeId)
    }
  },
  mounted () {
    this.updateLayout()
  },
  watch: {
    nodes: {
      deep: true,
      handler (value) {
        this.$emit('input', value)
        this.updateLayout()
      }
    },
    value: {
      deep: true,
      handler (val) {
        this.nodes = val
      }
    }
  },
  components: {
    SupplierNode
  }
}
</script>

<style lang='scss'>
.graph-editor {
  display: block;

  // margin: 0 auto;
  .path {
    fill: none;
    transition: d 0.5s;
    stroke-linejoin: round;
    stroke-width: 3;
    stroke: #aaa;
  }
  svg {
    // display:block;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    transition: width 1s;
    path {

    }
  }
  .svg-elements-move {
    transition: transform 0.5s;
  }
  .path-elements-move {
    transition: transform 0.5s;
  }
}

</style>
