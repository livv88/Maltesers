// Fetch cart on page load if user is authenticated
document.addEventListener('DOMContentLoaded', function() {
    fetchCart();
});
let book = null;
const CartItem = document.getElementsByClassName("CartItem");


function hideAbout() {
    const About = document.querySelector('.About');
    About.style.display = 'none';
}

function showAbout(bookId) {
    const About = document.querySelector('.About');
    About.style.display = 'block';
    book = bookId;
    fetch(`/api/book/${bookId}/`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("image").querySelector("img").src = data.image;
        document.getElementById("title").innerHTML = data.title;
        document.getElementById("author").innerHTML = data.author;
        document.getElementById("rating").innerHTML = data.rating;
        document.getElementById("genre").innerHTML = data.genre;
        document.getElementById("pages").innerHTML = data.pages;
        document.getElementById("language").innerHTML = data.language;
        document.getElementById("publication-date").innerHTML = data.publication_date;
        document.getElementById("paperback").innerHTML = data.paperback;
        document.getElementById("hardcover").innerHTML = data.hardcover;
        document.getElementById("price").innerHTML = data.price;
        document.getElementById("discount").innerHTML = data.discount;
        document.getElementById("shipping-cost").innerHTML = data.shipping_cost;
        document.getElementById("reviews").innerHTML = data.reviews;
        document.getElementById("description").innerHTML = data.description;
    });
}

function search(book) {
    //this is where you place the code to show books that sounds close to what theyre searching for...
}


async function addToCart() {
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ book_id: book, quantity: 1 })
        });
        const result = await response.json();
        if (result.success) {
            await fetchCart();
            hideAbout();
        } else {
            alert('Could not add to cart.');
        }
    } catch (err) {
        console.error('Error adding to cart:', err);
    }
}

async function fetchCart() {
    try {
        const response = await fetch('/api/cart/get/');
        const data = await response.json();
        const cartContainer = document.getElementById('CartItem');
        cartContainer.innerHTML = '';
        let subtotal = 0;
        data.items.forEach(item => {
            const template = document.createElement('div');
            template.className = 'CartItem';
            template.style.display = 'flex';
            template.innerHTML = `
                <img src="${item.image}" alt="${item.title}" class="cart-image">
                <div class="CartInfo">
                    <h2 class="cart-title">${item.title}</h2>
                    <p class="cart-author">${item.author}</p>
                    <div>
                        <span class="Discounted cart-discount">${item.discount}</span>
                        <span class="Cost cart-cost">${item.price}</span>
                    </div>
                </div>
                <div class="CartActions">
                    <button onclick="removeCartItem(${item.item_id})"><img src="/static/main/library/delete.svg" alt="delete"></button>
                    <span class="Amount">${item.quantity}</span>
                    <button onclick="addCartItem(${item.item_id})"><img src="/static/main/library/add.svg" alt="add"></button>
                </div>
            `;
            cartContainer.appendChild(template);
            subtotal += parseFloat(item.price) * item.quantity;
        });
        // Update order summary
        const summary = document.getElementById('Summary');
        if (summary) {
            const spans = summary.querySelectorAll('p span');
            if (spans.length > 0) spans[0].textContent = subtotal.toFixed(2) + '$'; // SubTotal
            if (spans.length > 2) spans[2].textContent = subtotal.toFixed(2) + '$'; // Total
        }
    } catch (err) {
        console.error('Error fetching cart:', err);
    }
}

async function removeCartItem(itemId) {
    try {
        const response = await fetch('/api/cart/remove/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ item_id: itemId })
        });
        const result = await response.json();
        if (result.success) {
            await fetchCart();
        } else {
            alert('Could not remove item.');
        }
    } catch (err) {
        console.error('Error removing cart item:', err);
    }
}

async function addCartItem(itemId) {
    try {
        const response = await fetch('/api/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ item_id: itemId, quantity: getCurrentQuantity(itemId) + 1 })
        });
        const result = await response.json();
        if (result.success) {
            await fetchCart();
        } else {
            alert('Could not update item.');
        }
    } catch (err) {
        console.error('Error updating cart item:', err);
    }
}

function getCurrentQuantity(itemId) {
    const cartItems = document.querySelectorAll('.CartItem');
    for (let item of cartItems) {
        if (item.querySelector('button[onclick^="removeCartItem"]').getAttribute('onclick').includes(itemId)) {
            return parseInt(item.querySelector('.Amount').textContent);
        }
    }
    return 1;
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
            return c.substring(name.length + 1, c.length);
        }
    }
    return '';
}

function remove(item) {
    item.closest('.CartItem').remove();
}

function add(item) {
    item.closest('.CartItem').querySelector('.Amount').textContent++;
}

function toggleTheme() {
    console.log("Toggling theme");
    document.body.classList.toggle('light-theme');
}

function signUp() {
    document.getElementById("Blur").style.display = "flex";
    document.querySelector(".SignUp").style.display = "block";
    document.querySelector(".LogIn").style.display = "none";
}

function logIn() {
    document.getElementById("Blur").style.display = "flex";
    document.querySelector(".LogIn").style.display = "block";
    document.querySelector(".SignUp").style.display = "none";
}

document.getElementById("Blur").addEventListener("click", function(e) {
    if (e.target.id === "Blur") { 
        this.style.display = "none";
        document.querySelector(".LogIn").style.display = "none";
        document.querySelector(".SignUp").style.display = "none";
    }
});
