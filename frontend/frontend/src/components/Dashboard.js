import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Button, Table, Alert } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const Dashboard = () => {
  const [trades, setTrades] = useState([]);
  const [showNewTradeForm, setShowNewTradeForm] = useState(false);

  const [newTrade, setNewTrade] = useState({
    symbol: '',
    stopLoss: '',
    profitPercent: '',
    amount: '',
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const getUserId = () => {
    const sessionData = localStorage.getItem('sessionData');

    if (!sessionData) return null;

    try {
      const parsedData = JSON.parse(sessionData);

      return (
        parsedData.id ||
        parsedData.userId ||
        parsedData.user_id ||
        parsedData?.data?.id ||
        parsedData?.user?.id ||
        null
      );
    } catch (error) {
      return null;
    }
  };

  const fetchTrades = async () => {
    try {
      setError('');

      const userId = getUserId();

      if (!userId) {
        setError('User session not found. Please login again.');
        return;
      }

      const response = await fetch(
        `http://127.0.0.1:5000/recent_trades?userId=${userId}`
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || 'Failed to fetch recent trades.');
        return;
      }

      setTrades(data.data || []);
    } catch (error) {
      setError('Backend connection failed while fetching trades.');
    }
  };

  useEffect(() => {
    fetchTrades();
  }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;

    setNewTrade((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleAddTrade = async (event) => {
    event.preventDefault();

    setError('');
    setSuccess('');

    const userId = getUserId();

    if (!userId) {
      setError('User session not found. Please login again.');
      return;
    }

    if (!newTrade.symbol || !newTrade.stopLoss || !newTrade.profitPercent || !newTrade.amount) {
      setError('Please fill all trade fields.');
      return;
    }

    const amount = parseFloat(newTrade.amount);
    const profitLimit = parseFloat(newTrade.profitPercent);
    const stopLoss = parseFloat(newTrade.stopLoss);

    if (Number.isNaN(amount) || Number.isNaN(profitLimit) || Number.isNaN(stopLoss)) {
      setError('Amount, profit, and stop loss must be valid numbers.');
      return;
    }

    const requestBody = {
      symbol: newTrade.symbol.trim().toUpperCase(),
      amount,
      profitLimit,
      stopLoss,
      userId,
      time: new Date().toISOString(),
    };

    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:5000/add_trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        setError(data?.message || data?.error || 'Failed to add trade.');
        return;
      }

      setSuccess('Trade added successfully.');
      setNewTrade({ symbol: '', stopLoss: '', profitPercent: '', amount: '' });
      setShowNewTradeForm(false);
      fetchTrades();
    } catch (error) {
      setError('Backend connection failed while adding trade.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusText = (status) => {
    if (status === 2 || status === '2') return 'Closed';
    if (status === 1 || status === '1') return 'Active';
    return 'Pending';
  };

  const getStatusClass = (status) => {
    if (status === 2 || status === '2') return 'status-pill status-closed';
    if (status === 1 || status === '1') return 'status-pill status-active';
    return 'status-pill status-pending';
  };

  const totalAmount = trades.reduce((sum, trade) => {
    return sum + Number(trade.amount || 0);
  }, 0);

  const activeTrades = trades.filter(
    (trade) => trade.status === 1 || trade.status === '1'
  ).length;

  const pendingTrades = trades.filter(
    (trade) =>
      trade.status !== 1 &&
      trade.status !== '1' &&
      trade.status !== 2 &&
      trade.status !== '2'
  ).length;

  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="section-padding">
        <div className="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
          <div>
            <h1 className="section-title">Trading Dashboard</h1>
            <p className="section-subtitle">
              Manage your trade entries, target profit, stop-loss, and AI prediction status.
            </p>
          </div>

          <Button className="btn-premium" onClick={() => setShowNewTradeForm(true)}>
            + Add New Trade
          </Button>
        </div>

        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <Row>
          <Col md={4} className="mb-3">
            <div className="stat-card">
              <div className="stat-label">Total Trades</div>
              <div className="stat-value">{trades.length}</div>
            </div>
          </Col>

          <Col md={4} className="mb-3">
            <div className="stat-card">
              <div className="stat-label">Pending Trades</div>
              <div className="stat-value">{pendingTrades}</div>
            </div>
          </Col>

          <Col md={4} className="mb-3">
            <div className="stat-card">
              <div className="stat-label">Total Amount</div>
              <div className="stat-value">₹{totalAmount.toLocaleString()}</div>
            </div>
          </Col>
        </Row>

        {showNewTradeForm && (
          <div className="premium-card card-padding mt-4">
            <h3 className="mb-3">Add New Trade</h3>

            <form onSubmit={handleAddTrade}>
              <Row>
                <Col md={6}>
                  <div className="mb-3">
                    <label className="form-label">Symbol</label>
                    <input
                      type="text"
                      className="form-control"
                      name="symbol"
                      placeholder="Example: BTC-USD"
                      value={newTrade.symbol}
                      onChange={handleInputChange}
                    />
                  </div>
                </Col>

                <Col md={6}>
                  <div className="mb-3">
                    <label className="form-label">Amount in INR</label>
                    <input
                      type="number"
                      step="any"
                      className="form-control"
                      name="amount"
                      placeholder="Example: 1000"
                      value={newTrade.amount}
                      onChange={handleInputChange}
                    />
                  </div>
                </Col>

                <Col md={6}>
                  <div className="mb-3">
                    <label className="form-label">Profit Target %</label>
                    <input
                      type="number"
                      step="any"
                      className="form-control"
                      name="profitPercent"
                      placeholder="Example: 10"
                      value={newTrade.profitPercent}
                      onChange={handleInputChange}
                    />
                  </div>
                </Col>

                <Col md={6}>
                  <div className="mb-3">
                    <label className="form-label">Stop Loss %</label>
                    <input
                      type="number"
                      step="any"
                      className="form-control"
                      name="stopLoss"
                      placeholder="Example: 5"
                      value={newTrade.stopLoss}
                      onChange={handleInputChange}
                    />
                  </div>
                </Col>
              </Row>

              <Button type="submit" className="btn-premium" disabled={loading}>
                {loading ? 'Saving...' : 'Save Trade'}
              </Button>

              <Button
                type="button"
                className="btn-ghost ms-2"
                onClick={() => setShowNewTradeForm(false)}
                disabled={loading}
              >
                Cancel
              </Button>
            </form>
          </div>
        )}

        <div className="premium-card card-padding mt-4">
          <h3>Recent Trades</h3>
          <p className="auth-muted">Active trades: {activeTrades}</p>

          <Table responsive className="trade-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Amount</th>
                <th>Profit Target</th>
                <th>Status</th>
                <th>Time</th>
              </tr>
            </thead>

            <tbody>
              {trades.length > 0 ? (
                trades.map((trade, index) => (
                  <tr key={index}>
                    <td><strong>{trade.symbol || '-'}</strong></td>
                    <td>₹{Number(trade.amount || 0).toLocaleString()}</td>
                    <td>{trade.position || trade.profitLimit || trade.profit_limit || '-'}</td>
                    <td>
                      <span className={getStatusClass(trade.status)}>
                        {getStatusText(trade.status)}
                      </span>
                    </td>
                    <td>{trade.createdAt || trade.created_at || trade.time || '-'}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="empty-state">
                    No trades found. Add your first trade.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </div>
      </Container>
    </div>
  );
};

export default Dashboard;