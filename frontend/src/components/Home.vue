<template lang='pug'>
.page
  .graphio
    el-tooltip(class="item" content="Save current state" placement="bottom")
      el-button.file-link(
        @click="download(JSON.stringify(form, null, ' '), 'dnaweaver_state.json')" icon='el-icon-download'
        circle)
    el-tooltip(class="item" content="Load a saved state" placement="bottom")
      el-button.file-link(
        @click='uploadStateDialogVisible = true'
        icon='el-icon-upload2'
        circle)
    el-tooltip(class="item" content="Load an example" placement="bottom")
      el-button.file-link(
        @click=''
        icon='el-icon-more'
        circle)
    el-dialog(title="", :visible.sync="uploadStateDialogVisible" width="80%")
      center
        h4 Upload a saved state
        el-upload(:file-list='stateUploadFile',
            :on-change='parseUploadedState',
            :multiple='false',
            :auto-upload="false",
            action=''
            drag)
          i.el-icon-upload
          .el-upload__text Drop a JSON file here or <em>click to upload</em>
    el-dialog(title="", :visible.sync="examplesDialogVisible" width="80%")
      center
        h4 Upload a saved state
        el-upload(:file-list='stateUploadFile',
          :on-change='parseUploadedState',
          :multiple='false',
          :auto-upload="false",
          action=''
          drag)
          i.el-icon-upload
          .el-upload__text Drop a JSON file here or <em>click to upload</em>
  .graph
    graph(v-model='form.graph', :options='options')
  .form
    el-form(label-width='120px')
      el-form-item(label='Optimization')
        el-select(v-model='form.optimization')
          el-option(value='cheapest', label='Cheapest plan')
          el-option(value='cheapest_with_deadline', label='Cheapest with deadline')
          el-option(value='fastest_under_budget', label='Fastest under budget')
      el-form-item(
        v-if="form.optimization == 'cheapest_with_deadline'"
        label='Deadline (days)')
        el-input-number(size='small' v-model='form.deadline')
      el-form-item(
        v-if="form.optimization == 'fastest_under_budget'"
        label='Budget ($)')
        el-input-number(size='small' v-model='form.budget')
    p.hello-there(v-if='form.budget >= 50000').
      Oh hello there ! Sounds like an interesting project.
      We should <a href="mailto:egf@ed.ac.uk?subject=Let's talk about my project"> get in touch.</a>
    h3 Upload a sequence
    files-uploader(v-model="form.sequence_file", :multiple='false')

    backend-querier(
      :form='form',
      :backendUrl='infos.backendUrl',
      :validateForm='validateForm',
      submitButtonText='Design',
      v-model='queryStatus')
    el-alert(v-if='queryStatus.requestError', :title="queryStatus.requestError",
             type="error", :closable="false")

      progress-bars(:bars='queryStatus.polling.data.bars', :order="['radius']"
                    v-if='queryStatus.polling.inProgress && queryStatus.polling.data')

      el-alert(v-show='queryStatus.requestError  && !queryStatus.polling.inProgress',
               :title="queryStatus.requestError",
               type="error",
               :closable="false")

    .results(v-if='!queryStatus.polling.inProgress && queryStatus.polling.data')
      .assembly-stats
        p Total cost: {{queryStatus.result.assembly_tree.price}}
      download-button(v-if='queryStatus.result.zip_file',
                      :filedata='queryStatus.result.zip_file')

</template>

<script>
import graph from './SupplyNetwork/Graph'
import download from 'downloadjs'
const defaultGraph = require('./SupplyNetwork/json/default-graph.json')
const defaultOptions = require('./SupplyNetwork/json/graph-options-fullsize.json')
var infos = {
  title: 'Generic Solver',
  navbarTitle: 'Generic Solver',
  path: 'generic_solver',
  description: '',
  backendUrl: 'start/generic_solver'
}

export default {
  name: 'Home',
  data () {
    return {
      form: {
        graph: JSON.parse(JSON.stringify(defaultGraph)),
        sequence_file: null,
        optimization: 'cheapest',
        deadline: 10,
        budget: 2000
      },
      uploadStateDialogVisible: false,
      examplesDialogVisible: false,
      stateUploadFile: [],
      options: JSON.parse(JSON.stringify(defaultOptions)),
      infos: infos,
      queryStatus: {
        polling: {},
        result: {},
        requestError: ''
      }
    }
  },
  components: {
    graph
  },
  methods: {
    download,
    parseUploadedState (evt) {
      var reader = new FileReader()
      var self = this
      reader.onload = function (e) {
        console.log(JSON.parse(e.target.result))
        self.form = JSON.parse(e.target.result)
        self.stateUploadFile = []
        self.uploadStateDialogVisible = false
      }
      reader.readAsBinaryString(evt.raw)
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
    },
    validateForm () {
      return []
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
    margin-bottom: 20px;
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
    text-align: center;
    .el-form {
      display: inline-block;
      /deep/ .el-form-item__content {
        text-align: left;
      }
    }
  }
  .hello-there {
    font-size: 0.8em;
  }
}

</style>
