import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import type { AppDispatch, RootState } from '../index';
import { CreditContract, Drawdown, Repayment, PortfolioCashflow, PortfolioMetrics } from '../../types';
import { portfolioApi } from '../../services/api';

interface PortfolioState {
  contracts: CreditContract[];
  drawdowns: Drawdown[];
  repayments: Repayment[];
  cashflow: PortfolioCashflow | null;
  metrics: PortfolioMetrics | null;
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

const initialState: PortfolioState = {
  contracts: [],
  drawdowns: [],
  repayments: [],
  cashflow: null,
  metrics: null,
  loading: false,
  error: null,
  lastUpdated: null,
};

// Асинхронные действия
export const fetchPortfolioData = createAsyncThunk(
  'portfolio/fetchData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await portfolioApi.getPortfolioData();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка загрузки данных портфеля');
    }
  }
);

export const fetchPortfolioMetrics = createAsyncThunk(
  'portfolio/fetchMetrics',
  async (versionId: string, { rejectWithValue }) => {
    try {
      const response = await portfolioApi.getPortfolioMetrics(versionId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка загрузки метрик');
    }
  }
);

export const fetchPortfolioCashflow = createAsyncThunk(
  'portfolio/fetchCashflow',
  async (versionId: string, { rejectWithValue }) => {
    try {
      const response = await portfolioApi.getPortfolioCashflow(versionId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка загрузки кэш-флоу');
    }
  }
);

export const refreshPortfolioData = createAsyncThunk(
  'portfolio/refreshData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await portfolioApi.refreshPortfolioData();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка обновления данных');
    }
  }
);

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    updateContract: (state, action: PayloadAction<CreditContract>) => {
      const index = state.contracts.findIndex(contract => contract.id === action.payload.id);
      if (index !== -1) {
        state.contracts[index] = action.payload;
      }
    },
    addContract: (state, action: PayloadAction<CreditContract>) => {
      state.contracts.push(action.payload);
    },
    removeContract: (state, action: PayloadAction<string>) => {
      state.contracts = state.contracts.filter(contract => contract.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchPortfolioData
      .addCase(fetchPortfolioData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPortfolioData.fulfilled, (state, action) => {
        state.loading = false;
        state.contracts = action.payload.contracts || [];
        state.drawdowns = action.payload.drawdowns || [];
        state.repayments = action.payload.repayments || [];
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(fetchPortfolioData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // fetchPortfolioMetrics
      .addCase(fetchPortfolioMetrics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPortfolioMetrics.fulfilled, (state, action) => {
        state.loading = false;
        state.metrics = action.payload;
      })
      .addCase(fetchPortfolioMetrics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // fetchPortfolioCashflow
      .addCase(fetchPortfolioCashflow.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPortfolioCashflow.fulfilled, (state, action) => {
        state.loading = false;
        state.cashflow = action.payload;
      })
      .addCase(fetchPortfolioCashflow.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // refreshPortfolioData
      .addCase(refreshPortfolioData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(refreshPortfolioData.fulfilled, (state, action) => {
        state.loading = false;
        state.contracts = action.payload.contracts || [];
        state.drawdowns = action.payload.drawdowns || [];
        state.repayments = action.payload.repayments || [];
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(refreshPortfolioData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setLoading,
  updateContract,
  addContract,
  removeContract,
} = portfolioSlice.actions;

export default portfolioSlice.reducer;
