<template lang='pug'>
.page
  .graph
    graph(v-model='form.graph', :options='options')
  .graphio
    el-button-group
      el-tooltip(class="item" content="Download this graph" placement="bottom")
        el-button.file-link(@click='downloadForm' icon='el-icon-download' circle)
      el-tooltip(class="item" content="Upload a graph" placement="bottom")
        el-button.file-link(@click='downloadForm' icon='el-icon-upload2' circle)
      el-tooltip(class="item" content="Load an example" placement="bottom")
        el-button.file-link(@click='downloadJson' icon='el-icon-more' circle)
  .form
    el-form(label-width='120px')
      el-form-item(label='Optimization')
        el-select(v-model='form.optimization')
          el-option(value='cheapest', label='Cheapest plan')
          el-option(value='cheapest_with_deadline', label='Cheapest with deadline')
          el-option(value='fastest_under_budget', label='Fastest under budget')
      el-form-item(v-if="form.optimization == 'cheapest_with_deadline'" label='Deadline')
        el-input-number(size='small' v-model='form.deadline')
      el-form-item(v-if="form.optimization == 'fastest_under_budget'" label='Deadline')
        el-input-number(size='small' v-model='form.budget')
    p.hello-there(v-if='budget >= 50000').
      Oh hello there ! Sounds like an interesting project.
      We should
      #[a(href="mailto:egf@ed.ac.uk?Subject=Let's%20talk%20about%20my%20project') get in touch.")]
    files-uploader(v-model="form.sequence_file", :multiple='false')
  .querier
    backend-querier
</template>

<script>
import graph from './SupplyNetwork/Graph'
import download from 'downloadjs'
const defaultGraph = require('./SupplyNetwork/json/default-graph.json')
const defaultOptions = require('./SupplyNetwork/json/graph-options-fullsize.json')

export default {
  name: 'Home',
  data () {
    return {
      options: JSON.parse(JSON.stringify(defaultOptions)),
      form: {
        graph: JSON.parse(JSON.stringify(defaultGraph)),
        sequence_file: null,
        optimization: 'cheapest',
        deadline: 10,
        budget: 2000,

      }
    }
  },
  components: {
    graph
  },
  methods: {
    downloadJson () {
      download(JSON.stringify(this.graph, null, ' '), 'design.json')
    },
    handlePreview (file) {
      var self = this
      var reader = new window.FileReader()
      reader.onloadend = function (ev) {
        if (ev.target.readyState === window.FileReader.DONE) {
          self.file = {
            name: name,
            content: ev.target.result
          }
        }
      }
      reader.readAsDataURL(file.raw)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='scss' scoped>

h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.page {
  .graphio {
    text-align: center;
  }
  .sequence-upload {
    text-align: center;
    margin: 40px auto;
    max-width: 500px;
  }
  .querier {
    margin: 0 auto;
    text-align: center;
    max-width: 500px;
  }
  .form {
    margin: 20px auto;
    width: 500px;
  }
}

</style>
