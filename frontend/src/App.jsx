import { useState, useEffect } from 'react'
import './App.css'

// Базовый URL вашего FastAPI бэкенда (настроенный через прокси или прямой)
const API_BASE = '/api'

export default function App() {
  // Состояние авторизации
  const [isReg, setIsReg] = useState(false)
  const [login, setLogin] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user')
    return saved ? JSON.parse(saved) : null // { userId, secret }
  })

  // Данные приложения
  const [products, setProducts] = useState([])
  const [cartItems, setCartItems] = useState([])

  // Форма нового товара
  const [newName, setNewName] = useState('')
  const [newPrice, setNewPrice] = useState('')

  // Ошибки и уведомления
  const [error, setError] = useState('')

  // Подгрузка данных при изменении статуса авторизации
  useEffect(() => {
    fetchProducts()
    if (user) {
      fetchCart()
    } else {
      setCartItems([])
    }
  }, [user])

  // --- API Запросы ---

  const handleAuth = async (e) => {
    e.preventDefault()
    setError('')
    const url = isReg ? `${API_BASE}/users` : `${API_BASE}/sessions`

    // Для регистрации отправляем JSON в body, для сессии — в Headers по вашей схеме
    const options = isReg
      ? {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ login, password })
        }
      : {
          method: 'POST',
          headers: { 'login': login, 'password': password }
        }

    try {
      const res = await fetch(url, options)
      if (!res.ok) throw new Error(isReg ? 'Пользователь уже существует' : 'Неверные данные входа')

      if (isReg) {
        setIsReg(false)
        alert('Успешная регистрация! Теперь войдите.')
      } else {
        const data = await res.json() // { user_id, secret }
        const loggedUser = { userId: data.user_id, secret: data.secret }
        setUser(loggedUser)
        localStorage.setItem('user', JSON.stringify(loggedUser))
      }
      setLogin('')
      setPassword('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products`)
      if (res.ok) {
        const data = await res.json()
        setProducts(data)
      }
    } catch (err) {
      console.error('Ошибка загрузки товаров:', err)
    }
  }

  const fetchCart = async () => {
    if (!user) return
    try {
      const res = await fetch(`${API_BASE}/users/${user.userId}/cart/items`, {
        headers: { 'session-secret': user.secret }
      })
      if (res.ok) {
        const data = await res.json()
        setCartItems(data)
      }
    } catch (err) {
      console.error('Ошибка загрузки корзины:', err)
    }
  }

  const handleCreateProduct = async (e) => {
    e.preventDefault()
    if (!newName || !newPrice) return

    try {
      const res = await fetch(`${API_BASE}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName, price: Number(newPrice) })
      })
      if (res.ok) {
        setNewName('')
        setNewPrice('')
        fetchProducts()
      }
    } catch (err) {
      console.error('Не удалось создать товар:', err)
    }
  }

  return (
    <div className="app-container">
      {/* Шапка сайта */}
      <header className="main-header">
        <div className="logo">⚡ МикроСтор</div>
        <div className="auth-status">
          {user ? (
            <div className="user-info">
              <span>ID Пользователя: <strong>{user.userId}</strong></span>
              <button className="btn-secondary" onClick={handleLogout}>Выйти</button>
            </div>
          ) : (
            <span className="guest-badge">Гостевой режим</span>
          )}
        </div>
      </header>

      <main className="main-content">
        {/* Блок авторизации, если пользователь не вошел */}
        {!user && (
          <section className="card auth-card">
            <h2>{isReg ? 'Регистрация' : 'Вход в аккаунт'}</h2>
            <form onSubmit={handleAuth} className="vertical-form">
              <input
                type="text"
                placeholder="Логин"
                value={login}
                onChange={e => setLogin(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
              <button type="submit" className="btn-primary">
                {isReg ? 'Зарегистрироваться' : 'Войти'}
              </button>
              {error && <p className="error-text">{error}</p>}
            </form>
            <button className="btn-link" onClick={() => setIsReg(!isReg)}>
              {isReg ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Создать'}
            </button>
          </section>
        )}

        {/* Каталог товаров */}
        <section className="card catalog-section">
          <div className="section-header">
            <h2>Каталог товаров</h2>
            <span className="count-tag">Всего: {products.length}</span>
          </div>

          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-item">
                <div className="product-info">
                  <span className="product-id">#{product.id}</span>
                  <span className="product-name">{product.name}</span>
                </div>
                <strong className="product-price">{product.price} ₽</strong>
              </div>
            ))}
            {products.length === 0 && <p className="empty-text">Товары еще не добавлены.</p>}
          </div>

          {/* Форма добавления товара */}
          <form onSubmit={handleCreateProduct} className="horizontal-form row-add-product">
            <input
              type="text"
              placeholder="Название товара"
              value={newName}
              onChange={e => setNewName(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Цена"
              value={newPrice}
              onChange={e => setNewPrice(e.target.value)}
              required
            />
            <button type="submit" className="btn-accent">+ Добавить</button>
          </form>
        </section>

        {/* Корзина (отображается только у авторизованных) */}
        {user && (
          <section className="card cart-section">
            <div className="section-header">
              <h2>Ваша корзина</h2>
              <span className="count-tag bg-accent">Элементов: {cartItems.length}</span>
            </div>
            <div className="cart-list">
              {cartItems.map(item => {
                // Ищем имя товара по его id из общего каталога для красивого вывода
                const prodDetails = products.find(p => p.id === item.product_id)
                return (
                  <div key={item.id} className="cart-item">
                    <span>Запись в корзине: <strong>#{item.id}</strong></span>
                    <span>Товар: <strong>{prodDetails ? prodDetails.name : `ID ${item.product_id}`}</strong></span>
                  </div>
                )
              })}
              {cartItems.length === 0 && (
                <p className="empty-text">
                  Корзина пуста. Добавьте элементы через бэкенд (в OpenAPI нет эндпоинта на добавление).
                </p>
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}
