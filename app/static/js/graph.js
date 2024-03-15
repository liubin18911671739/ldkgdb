function visualizeGraph(data, containerID) {
  // 创建 Vis.js 图形实例
  const container = document.getElementById(containerID);
  const options = {
    layout: {
      hierarchical: false,
    },
    edges: {
      arrows: {
        to: true,
      },
    },
  };
  const network = new vis.Network(container, data, options);
}

function executeQuery(query) {
  // 发送 AJAX 请求执行 Cypher 查询
  fetch("/graph/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  })
    .then((response) => response.json())
    .then((data) => {
      // 在容器中渲染查询结果
      visualizeGraph(data, "visualization");
    })
    .catch((error) => {
      console.error("Error executing query:", error);
    });
}

function handleMergeOperation(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const label = formData.get("label");
  const properties = JSON.parse(formData.get("properties"));

  // 发送 AJAX 请求执行合并操作
  fetch("/graph/merge", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ label, properties }),
  })
    .then((response) => response.json())
    .then((data) => {
      // 在容器中渲染操作结果
      visualizeGraph(data, "visualization");
    })
    .catch((error) => {
      console.error("Error merging node:", error);
    });
}

function handleDeleteOperation(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const label = formData.get("label");
  const properties = JSON.parse(formData.get("properties"));

  // 发送 AJAX 请求执行删除操作
  fetch("/graph/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ label, properties }),
  })
    .then((response) => response.json())
    .then((data) => {
      // 在容器中渲染操作结果
      visualizeGraph(data, "visualization");
    })
    .catch((error) => {
      console.error("Error deleting node:", error);
    });
}

// 事件监听器
document.querySelectorAll('form[data-operation="query"]').forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const query = formData.get("query");
    executeQuery(query);
  });
});

document.querySelectorAll('form[data-operation="merge"]').forEach((form) => {
  form.addEventListener("submit", handleMergeOperation);
});

document.querySelectorAll('form[data-operation="delete"]').forEach((form) => {
  form.addEventListener("submit", handleDeleteOperation);
});
