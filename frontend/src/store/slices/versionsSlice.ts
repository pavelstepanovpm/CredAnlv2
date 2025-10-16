import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { CalculationVersion } from '../../types';
import { versionsApi } from '../../services/api';

interface VersionsState {
  versions: CalculationVersion[];
  activeVersion: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: VersionsState = {
  versions: [],
  activeVersion: null,
  loading: false,
  error: null,
};

// Асинхронные действия
export const fetchVersions = createAsyncThunk(
  'versions/fetchVersions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await versionsApi.getVersions();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка загрузки версий');
    }
  }
);

export const createVersion = createAsyncThunk(
  'versions/createVersion',
  async (versionData: Partial<CalculationVersion>, { rejectWithValue }) => {
    try {
      const response = await versionsApi.createVersion(versionData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка создания версии');
    }
  }
);

export const updateVersion = createAsyncThunk(
  'versions/updateVersion',
  async ({ id, data }: { id: string; data: Partial<CalculationVersion> }, { rejectWithValue }) => {
    try {
      const response = await versionsApi.updateVersion(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка обновления версии');
    }
  }
);

export const deleteVersion = createAsyncThunk(
  'versions/deleteVersion',
  async (id: string, { rejectWithValue }) => {
    try {
      await versionsApi.deleteVersion(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка удаления версии');
    }
  }
);

export const setActiveVersion = createAsyncThunk(
  'versions/setActiveVersion',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await versionsApi.setActiveVersion(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка установки активной версии');
    }
  }
);

export const compareVersions = createAsyncThunk(
  'versions/compareVersions',
  async ({ version1Id, version2Id }: { version1Id: string; version2Id: string }, { rejectWithValue }) => {
    try {
      const response = await versionsApi.compareVersions(version1Id, version2Id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Ошибка сравнения версий');
    }
  }
);

const versionsSlice = createSlice({
  name: 'versions',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setActiveVersionLocal: (state, action: PayloadAction<string>) => {
      state.activeVersion = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchVersions
      .addCase(fetchVersions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVersions.fulfilled, (state, action) => {
        state.loading = false;
        state.versions = action.payload;
        // Устанавливаем активную версию
        const activeVersion = action.payload.find(v => v.status === 'active');
        if (activeVersion) {
          state.activeVersion = activeVersion.id;
        }
      })
      .addCase(fetchVersions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // createVersion
      .addCase(createVersion.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createVersion.fulfilled, (state, action) => {
        state.loading = false;
        state.versions.push(action.payload);
      })
      .addCase(createVersion.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // updateVersion
      .addCase(updateVersion.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateVersion.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.versions.findIndex(v => v.id === action.payload.id);
        if (index !== -1) {
          state.versions[index] = action.payload;
        }
      })
      .addCase(updateVersion.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // deleteVersion
      .addCase(deleteVersion.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteVersion.fulfilled, (state, action) => {
        state.loading = false;
        state.versions = state.versions.filter(v => v.id !== action.payload);
        if (state.activeVersion === action.payload) {
          state.activeVersion = null;
        }
      })
      .addCase(deleteVersion.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // setActiveVersion
      .addCase(setActiveVersion.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(setActiveVersion.fulfilled, (state, action) => {
        state.loading = false;
        state.activeVersion = action.payload.id;
        // Обновляем статус всех версий
        state.versions = state.versions.map(v => ({
          ...v,
          status: v.id === action.payload.id ? 'active' : 'draft'
        }));
      })
      .addCase(setActiveVersion.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setLoading,
  setActiveVersionLocal,
} = versionsSlice.actions;

export default versionsSlice.reducer;

