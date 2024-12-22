function likePost(postId) {
    fetch(`/like/${postId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`likes-count-${postId}`).innerText = data.likes_count;
    })
    .catch(error => console.error('Error:', error));
}
