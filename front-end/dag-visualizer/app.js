/**
* DAG Visualizer - Alpine.js Application
*/


// =============================================================================
// DAG DATA
// =============================================================================


const DAG_DATA = {
  dag_id: "my_etl_pipeline",
  schedule_interval: "0 6 * * *",
  start_date: "2026-01-01",
  catchup: false,
  tags: ["etl", "production"],
  tasks: [
    {
      task_id: "extract_users",
      operator: "PythonOperator",
      depends_on: [],
      status: "completed",
      started_at: "2026-01-01 06:00:05",
      completed_at: "2026-01-01 06:01:00",
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:00:05] INFO: Starting extract_users task",
        "[2026-01-01 06:00:06] INFO: Connecting to PostgreSQL database",
        "[2026-01-01 06:00:08] INFO: Executing query: SELECT * FROM users WHERE updated_at > '2025-12-31'",
        "[2026-01-01 06:00:45] INFO: Retrieved 125,432 rows",
        "[2026-01-01 06:00:55] INFO: Writing to S3: s3://data-lake/raw/users/2026-01-01/",
        "[2026-01-01 06:01:00] INFO: Task completed successfully"
      ]
    },
    {
      task_id: "extract_orders",
      operator: "PythonOperator",
      depends_on: [],
      status: "completed",
      started_at: "2026-01-01 06:00:10",
      completed_at: "2026-01-01 06:02:00",
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:00:10] INFO: Starting extract_orders task",
        "[2026-01-01 06:00:12] INFO: Connecting to PostgreSQL database",
        "[2026-01-01 06:00:15] INFO: Executing query: SELECT * FROM orders WHERE created_at > '2025-12-31'",
        "[2026-01-01 06:01:30] INFO: Retrieved 892,156 rows",
        "[2026-01-01 06:01:50] INFO: Writing to S3: s3://data-lake/raw/orders/2026-01-01/",
        "[2026-01-01 06:02:00] INFO: Task completed successfully"
      ]
    },
    {
      task_id: "extract_products",
      operator: "S3ToRedshiftOperator",
      depends_on: [],
      status: "completed",
      started_at: "2026-01-01 06:00:00",
      completed_at: "2026-01-01 06:01:30",
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:00:00] INFO: Starting S3 to Redshift transfer",
        "[2026-01-01 06:00:05] INFO: Source: s3://product-catalog/exports/latest/",
        "[2026-01-01 06:00:10] INFO: Destination: redshift://warehouse/staging.products",
        "[2026-01-01 06:01:20] INFO: Transferred 45,678 records",
        "[2026-01-01 06:01:30] INFO: Transfer completed successfully"
      ]
    },
    {
      task_id: "validate_users",
      operator: "PythonOperator",
      depends_on: ["extract_users"],
      status: "completed",
      started_at: "2026-01-01 06:01:05",
      completed_at: "2026-01-01 06:03:00",
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:01:05] INFO: Starting validation for users dataset",
        "[2026-01-01 06:01:10] INFO: Loading schema from s3://schemas/users_v2.json",
        "[2026-01-01 06:01:15] INFO: Validating 125,432 records",
        "[2026-01-01 06:02:30] INFO: Schema validation passed",
        "[2026-01-01 06:02:45] INFO: Null check passed: 0 null values in required fields",
        "[2026-01-01 06:03:00] INFO: Validation completed successfully"
      ]
    },
    {
      task_id: "validate_orders",
      operator: "PythonOperator",
      depends_on: ["extract_orders"],
      status: "failed",
      started_at: "2026-01-01 06:02:05",
      completed_at: null,
      failed_at: "2026-01-01 06:04:00",
      error_message: "Schema validation failed: missing 'order_date' column",
      logs: [
        "[2026-01-01 06:02:05] INFO: Starting validation for orders dataset",
        "[2026-01-01 06:02:10] INFO: Loading schema from s3://schemas/orders_v3.json",
        "[2026-01-01 06:02:15] INFO: Validating 892,156 records",
        "[2026-01-01 06:03:30] WARN: Column mismatch detected",
        "[2026-01-01 06:03:45] ERROR: Missing required column: 'order_date'",
        "[2026-01-01 06:03:50] ERROR: Expected columns: [order_id, user_id, order_date, total_amount, status]",
        "[2026-01-01 06:03:55] ERROR: Found columns: [order_id, user_id, total_amount, status]",
        "[2026-01-01 06:04:00] FATAL: Schema validation failed: missing 'order_date' column"
      ]
    },
    {
      task_id: "transform_users",
      operator: "SparkSubmitOperator",
      depends_on: ["validate_users"],
      status: "running",
      started_at: "2026-01-01 06:03:10",
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:03:10] INFO: Submitting Spark job: transform_users_v2.py",
        "[2026-01-01 06:03:15] INFO: Spark cluster: emr-cluster-prod-01",
        "[2026-01-01 06:03:20] INFO: Job ID: spark-2026010106031500001",
        "[2026-01-01 06:03:25] INFO: Allocated 8 executors with 16GB memory each",
        "[2026-01-01 06:03:30] INFO: Reading from s3://data-lake/raw/users/2026-01-01/",
        "[2026-01-01 06:05:00] INFO: Processing stage 1/3: Deduplication",
        "[2026-01-01 06:07:00] INFO: Processing stage 2/3: Normalization",
        "[2026-01-01 06:09:00] INFO: Processing stage 3/3: Enrichment (in progress...)"
      ]
    },
    {
      task_id: "transform_orders",
      operator: "SparkSubmitOperator",
      depends_on: ["validate_orders"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    },
    {
      task_id: "transform_products",
      operator: "SparkSubmitOperator",
      depends_on: ["extract_products"],
      status: "completed",
      started_at: "2026-01-01 06:01:35",
      completed_at: "2026-01-01 06:05:00",
      failed_at: null,
      error_message: null,
      logs: [
        "[2026-01-01 06:01:35] INFO: Submitting Spark job: transform_products_v1.py",
        "[2026-01-01 06:01:40] INFO: Spark cluster: emr-cluster-prod-01",
        "[2026-01-01 06:01:45] INFO: Job ID: spark-2026010106014500002",
        "[2026-01-01 06:02:00] INFO: Reading from redshift://warehouse/staging.products",
        "[2026-01-01 06:03:00] INFO: Applying category mappings",
        "[2026-01-01 06:04:00] INFO: Calculating price metrics",
        "[2026-01-01 06:04:45] INFO: Writing to s3://data-lake/curated/products/",
        "[2026-01-01 06:05:00] INFO: Task completed successfully"
      ]
    },
    {
      task_id: "join_user_orders",
      operator: "SparkSubmitOperator",
      depends_on: ["transform_users", "transform_orders"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    },
    {
      task_id: "enrich_with_products",
      operator: "SparkSubmitOperator",
      depends_on: ["join_user_orders", "transform_products"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    },
    {
      task_id: "load_to_warehouse",
      operator: "RedshiftSQLOperator",
      depends_on: ["enrich_with_products"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    },
    {
      task_id: "update_dashboard",
      operator: "HttpOperator",
      depends_on: ["load_to_warehouse"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    },
    {
      task_id: "send_notification",
      operator: "SlackWebhookOperator",
      depends_on: ["load_to_warehouse"],
      status: "pending",
      started_at: null,
      completed_at: null,
      failed_at: null,
      error_message: null,
      logs: []
    }
  ]
};


// =============================================================================
// CONSTANTS
// =============================================================================


const STATUS_COLORS = {
  completed: { background: '#dafbe1', border: '#1a7f37' },
  running: { background: '#ddf4ff', border: '#0969da' },
  pending: { background: '#ffffff', border: '#57606a' },
  failed: { background: '#ffebe9', border: '#cf222e' }
};


const SPINNER_FRAMES = ['◐', '◓', '◑', '◒'];


// =============================================================================
// ALPINE.JS COMPONENT
// =============================================================================


function dagApp() {
  return {
    // State
    dagData: DAG_DATA,
    modalOpen: false,
    selectedTask: null,
    nodes: null,
    network: null,


    // Initialize
    init() {
      this.renderGraph();
      this.startSpinnerAnimation();
    },


    // Open modal for a task
    openModal(taskId) {
      this.selectedTask = this.dagData.tasks.find(t => t.task_id === taskId);
      this.modalOpen = true;
    },


    // Calculate task duration
    calculateDuration(task) {
      if (!task?.started_at) return 'N/A';

      const start = new Date(task.started_at);
      const end = task.completed_at
        ? new Date(task.completed_at)
        : task.failed_at
          ? new Date(task.failed_at)
          : new Date();

      const diffMs = end - start;
      const diffSecs = Math.floor(diffMs / 1000);
      const mins = Math.floor(diffSecs / 60);
      const secs = diffSecs % 60;

      return task.status === 'running'
        ? `${mins}m ${secs}s (running)`
        : `${mins}m ${secs}s`;
    },


    // Get log level class
    getLogLevel(log) {
      if (log.includes('FATAL')) return 'fatal';
      if (log.includes('ERROR')) return 'error';
      if (log.includes('WARN')) return 'warn';
      if (log.includes('INFO')) return 'info';
      return '';
    },


    // Check if task is a leaf node
    isLeafNode(taskId) {
      const allDependencies = new Set(this.dagData.tasks.flatMap(t => t.depends_on));
      return !allDependencies.has(taskId);
    },


    // Get task icon
    getTaskIcon(task) {
      if (task.status === 'running') return '◐ ';
      if (task.depends_on.length === 0) return '⚡ ';
      if (this.isLeafNode(task.task_id)) return '🍃 ';
      return '';
    },


    // Get task tooltip
    getTaskTooltip(task) {
      if (task.error_message) return `Error: ${task.error_message}`;
      if (task.depends_on.length === 0) return 'Root node (no dependencies)';
      if (this.isLeafNode(task.task_id)) return 'Leaf node (end of pipeline)';
      return 'Depends on: ' + task.depends_on.join(', ');
    },


    // Create vis.js nodes
    createNodes() {
      return new vis.DataSet(
        this.dagData.tasks.map(task => {
          const status = task.status || 'pending';
          const colors = STATUS_COLORS[status];
          const icon = this.getTaskIcon(task);


          return {
            id: task.task_id,
            label: `${icon}${task.task_id}\n<i>${task.operator}</i>`,
            title: this.getTaskTooltip(task),
            shape: 'box',
            color: {
              background: colors.background,
              border: colors.border,
              highlight: { background: '#ffffff', border: colors.border },
              hover: { background: '#ffffff', border: colors.border }
            },
            font: {
              color: '#24292f',
              face: "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace",
              size: 13,
              multi: 'html',
              align: 'center',
              ital: {
                color: '#6e7781',
                size: 10,
                face: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                mod: 'italic'
              }
            },
            borderWidth: 2,
            borderWidthSelected: 3,
            margin: { top: 16, bottom: 16, left: 20, right: 20 },
            shadow: false
          };
        })
      );
    },


    // Create vis.js edges
    createEdges() {
      return new vis.DataSet(
        this.dagData.tasks.flatMap(task =>
          task.depends_on.map(dep => ({
            from: dep,
            to: task.task_id,
            arrows: { to: { enabled: true, scaleFactor: 0.6, type: 'arrow' } },
            color: { color: '#8c959f', highlight: '#0969da', hover: '#0969da' },
            width: 1.5,
            smooth: { type: 'cubicBezier', forceDirection: 'horizontal', roundness: 0.4 }
          }))
        )
      );
    },


    // Render the graph
    renderGraph() {
      this.nodes = this.createNodes();
      const edges = this.createEdges();


      const container = document.getElementById('graph');
      const data = { nodes: this.nodes, edges };
      const options = {
        layout: {
          hierarchical: {
            direction: 'LR',
            sortMethod: 'directed',
            levelSeparation: 220,
            nodeSpacing: 100,
            treeSpacing: 100
          }
        },
        physics: false,
        interaction: {
          hover: true,
          zoomView: true,
          dragView: true,
          tooltipDelay: 100
        }
      };


      this.network = new vis.Network(container, data, options);


      // Click handler - use arrow function to preserve 'this'
      this.network.on('click', (params) => {
        if (params.nodes.length > 0) {
          this.openModal(params.nodes[0]);
        }
      });
    },


    // Animate spinner for running tasks
    startSpinnerAnimation() {
      const runningTasks = this.dagData.tasks.filter(t => t.status === 'running');
      if (runningTasks.length === 0) return;


      let frame = 0;
      setInterval(() => {
        frame = (frame + 1) % SPINNER_FRAMES.length;
        runningTasks.forEach(task => {
          this.nodes.update({
            id: task.task_id,
            label: `${SPINNER_FRAMES[frame]} ${task.task_id}\n<i>${task.operator}</i>`
          });
        });
      }, 150);
    }
  };
}



