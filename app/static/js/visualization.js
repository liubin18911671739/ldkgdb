function visualizeGraph(data, containerID) {
  // 创建 Vis.js 网络实例
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

// 从 URL 查询参数中获取结果数据
const urlParams = new URLSearchParams(window.location.search);
const resultData = urlParams.get("result");

if (resultData) {
  // 解码并解析结果数据
  const parsedData = JSON.parse(decodeURIComponent(resultData));

  // 在页面加载时渲染图形可视化
  window.addEventListener("load", () => {
    visualizeGraph(parsedData, "visualization");
  });
}
