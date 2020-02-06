<template lang='pug'>
.page
  .graphio
    el-tooltip(class="item" content="Download current state for later use" placement="bottom")
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
        @click='examplesDialogVisible = true'
        ) Load an example
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
        //- el-row(:gutter='10', style='width: 90%; max-width:1000px;')
        el-carousel(type='card', height="500px" :autoplay='false',
                    :loop='false' :initial-index='1')
          el-carousel-item
            file-example(filename='Basic Example',
                          @input="loadExample",
                          fileHref='/static/examples/basic_example/basic_example.json',
                          imgSrc='/static/examples/basic_example/basic_example.png')
              p.
                A very simple example for quick tests. One sequence, one bit of which can be
                synthesized by a company, and the other bit by other.
          el-carousel-item
            file-example(filename='3-step Assembly',
                        @input="loadExample",
                        fileHref='/static/examples/three_step/three_step.json',
                        imgSrc='/static/examples/three_step/three_step.png')
              p.
                A 50kb sequence to be built from large fragments or from oligos via a 3-step assembly.
                Some parts of the sequence can also be obtained from E. coli via PCR.
                #[a(href="https://www.nature.com/articles/srep10655") Tsuge et al. ]
                managed to assemble this sequence in a one-step assembly of fifty 1kb
                fragments, digested by type-IIs enzymes. This required a very careful
                selection of enzyme overhangs.
          el-carousel-item
            file-example(filename='Domestication Example',
                        @input="loadExample",
                        fileHref='/static/examples/domestication/domestication.json',
                        imgSrc='/static/examples/domestication/domestication.png')
              p.
                DNA Weaver can be used for many things, at the condition of designing
                the right supply network. Here we show how to use DNA Weaver to create
                PCR plans for part domestication.
                A gene sequence of E. coli has been optimized to be rid of two BsmBI
                sites in the wildtype sequence. We will construct the optimized gene
                by assembling 3 PCR products from the E. coli chromosome. The PCRs
                are done with custom primers whose non-annealing parts incur sequence
                modifications and remove the BsmBI sites via synonymous codon juggling.
          el-carousel-item
            file-example(filename='Parts Reuse Example',
                        @input="loadExample",
                        fileHref='/static/examples/parts_reuse/parts_reuse.json',
                        imgSrc='/static/examples/parts_reuse/parts_reuse.png')
              p.
                In this example a sequence is made via Golden Gate from parts
                of different origins: some are bought from a commercial provider,
                some are taken from the EMMA assembly standard, and some are
                extracted from a genome.
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

    .querier(style='max-width: 400px; width: 90%')
      backend-querier(
        :form='form',
        :backendUrl='infos.backendUrl',
        :validateForm='validateForm',
        submitButtonText='Compute an assembly plan',
        v-model='queryStatus')
  el-alert(v-show='queryStatus.requestError  && !queryStatus.polling.inProgress',
           :title="queryStatus.requestError",
           type="error",
           :closable="false")

  progress-bars(:bars='queryStatus.polling.data.bars', :order="orderedProgressBars",
                v-if='queryStatus.polling.inProgress && queryStatus.polling.data')
  .pre-results(v-if='queryStatus.polling.inProgress && queryStatus.polling.data')
    center
      h2(v-if="queryStatus.polling.data.price") Assembly Plan
      .assembly-stats
        p(v-if="queryStatus.polling.data.price").
          Total cost: {{queryStatus.polling.data.price.toFixed(0)}} $
        p(v-if="queryStatus.polling.data.lead_time").
          Lead time: {{queryStatus.polling.data.lead_time.toFixed(0)}} days

  .results(v-if='!queryStatus.polling.inProgress && queryStatus.polling.data')
    .assembly-plan(v-if='queryStatus.result.accepted')
      h2 Assembly Plan
      .assembly-stats
        p Total cost: {{queryStatus.result.assembly_tree.price.toFixed(0)}} $
        p Lead time: {{queryStatus.result.assembly_tree.lead_time.toFixed(0)}} days
        p Complexity: {{assemblyTreeOperations}} operations
    p(v-if='!queryStatus.result.accepted').
      No assembly plan found. Try editing the sequence or the supply graph.
    download-button(v-if='queryStatus.result.assembly_report',
                    text='Full assembly report',
                    :filedata='queryStatus.result.assembly_report')
  .assembly-figure(v-if='queryStatus.polling.data')
    center
      img(v-if='queryStatus.polling.data.figure_data',
          :src='queryStatus.polling.data.figure_data',
          style='max-width: 700px;')
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
        self.stateUploadFile = []
        self.form = JSON.parse(e.target.result)
        self.uploadStateDialogVisible = false
      }
      reader.readAsBinaryString(evt.raw)
    },
    validateForm () {
      return []
    },
    loadExample (file) {
      this.examplesDialogVisible = false
      this.form = JSON.parse(atob(file.content.split('base64,')[1]))
    }
  },
  computed: {
    assemblyTreeOperations () {
      if (!this.queryStatus.result) {
        return 0
      }
      var total = 0
      function explore (plan) {
        total++
        if (plan.assembly_plan) {
          plan.assembly_plan.map(explore)
        }
      }
      explore(this.queryStatus.result.assembly_tree)
      return total
    },
    orderedProgressBars () {
      if (this.queryStatus.polling.data && this.queryStatus.polling.data.bars) {
        var result = []
        Object.keys(this.queryStatus.polling.data.bars).map(function (s) {
          if (s.indexOf('segment') === -1) {
            result.push(s)
          }
        })
        console.log(result)
        return result
      } else {
        return []
      }
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
  .results {
    text-align: center;
    margin-top: 50px;
  }
}

</style>
