document.addEventListener("DOMContentLoaded", function () {
    const deleteTaskBtns = document.querySelectorAll(".delete-task-btn");
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteTaskModal"));
    const taskTitleSpan = document.getElementById("taskTitle");
    const deleteTaskForm = document.getElementById("deleteTaskForm");

    deleteTaskBtns.forEach((btn) => {
        btn.addEventListener("click", function (event) {
            event.preventDefault();
            const taskId = this.getAttribute("data-task-id");
            const taskTitle = this.getAttribute("data-task-title");

            taskTitleSpan.textContent = taskTitle;
            deleteTaskForm.action = `/tasks/delete/${taskId}/`;
            deleteModal.show();
        });
    });
});