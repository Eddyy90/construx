function handle_unread_notifications(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    for (let menu of menus) {
        menu.innerHTML = "";
    }

    var dateFormatter = new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    for (let msg of data.unread_list) { 
        var notification = document.createElement('a');
        if (msg.data?.link) {
            notification.setAttribute('href', msg.data.link);
        }
        var formattedTimestamp = dateFormatter.format(new Date(msg.timestamp));
        var description = [msg.verb].filter(m => !!m).join(' ');
        notification.classList.add('dropdown-item', 'd-flex');
        notification.setAttribute('data-id', msg.slug);

        notification.innerHTML = `
            <div class="position relative">
                <div>
                    <div class="notifyimg bg-primary brround box-shadow-primary ">
                        <i class="fe fe-mail"></i>
                    </div>
                    <div class="mt-1 w-80">
                        <h5 class="notification-label text-wrap">
                            ${description} ${msg.action_object || ""}
                        </h5>
                        <span class="notification-subtext">${formattedTimestamp}</span>
                    </div>
                </div>
                <span  class="btn-sm btn-icon btn-light markasread position-absolute top-0 end-0">
                    <i class="fe fe-x"></i>
                </span>
            </div>
        `;
        for (let menu of menus) {
            menu.appendChild(notification);
        }
    }
}

$('.notifications-menu').on('click', '.markasread', function(event) {
    var notificationElement = $(this).closest('.dropdown-item');
    var notificationSlug = notificationElement.data('id');
    event.stopPropagation();
    event.preventDefault();

    $.ajax({
        url: `/notifications/mark-as-read/${notificationSlug}/`,
        type: 'GET',
        success: function() {
            notificationElement.addClass('disabled');
            notificationElement.css('pointer-events', 'none');
            notificationElement.css('background-color', '#d3d3d3');
            notificationElement.slideUp('slow', function() {
                notificationElement.remove();
            });
        },
        error: function(xhr, status, error) {
            console.error("Erro ao marcar como lido:", error);
        }
    });
});