import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Box,
  Button,
  Divider,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayArrowIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { setActiveVersionLocal } from '../store/slices/versionsSlice';
import { CalculationVersion } from '../types';

export const VersionsPanel: React.FC = () => {
  const dispatch = useDispatch();
  const { versions, activeVersion } = useSelector((state: RootState) => state.versions);

  const handleSetActive = (versionId: string) => {
    dispatch(setActiveVersionLocal(versionId));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'draft':
        return 'secondary';
      case 'archived':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return 'Активная';
      case 'draft':
        return 'Черновик';
      case 'archived':
        return 'Архивная';
      default:
        return status;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'base':
        return 'Базовая';
      case 'scenario':
        return 'Сценарная';
      default:
        return type;
    }
  };

  return (
    <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#ffffff' }}>
            Версии расчетов
          </Typography>
          <Button
            variant="contained"
            size="small"
            startIcon={<AddIcon />}
            sx={{
              background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
              },
            }}
          >
            Создать
          </Button>
        </Box>

        <Divider sx={{ borderColor: '#555', mb: 2 }} />

        <List sx={{ p: 0 }}>
          {versions.slice(0, 5).map((version: CalculationVersion) => (
            <ListItem
              key={version.id}
              sx={{
                backgroundColor: activeVersion === version.id ? '#0066cc20' : 'transparent',
                borderRadius: 1,
                mb: 1,
                border: activeVersion === version.id ? '1px solid #0066cc' : '1px solid transparent',
              }}
            >
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="subtitle2" sx={{ color: '#ffffff', fontWeight: 600 }}>
                      {version.name}
                    </Typography>
                    <Chip
                      label={getTypeLabel(version.version_type)}
                      size="small"
                      sx={{
                        backgroundColor: version.version_type === 'base' ? '#0066cc20' : '#ffaa0020',
                        color: version.version_type === 'base' ? '#0066cc' : '#ffaa00',
                        border: '1px solid',
                        borderColor: version.version_type === 'base' ? '#0066cc' : '#ffaa00',
                        fontSize: '10px',
                        height: 20,
                      }}
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="body2" sx={{ color: '#cccccc', mb: 0.5 }}>
                      {version.description || 'Без описания'}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={getStatusLabel(version.status)}
                        size="small"
                        color={getStatusColor(version.status) as any}
                        sx={{ fontSize: '10px', height: 20 }}
                      />
                      <Typography variant="caption" sx={{ color: '#999999' }}>
                        {new Date(version.created_at).toLocaleDateString('ru-RU')}
                      </Typography>
                    </Box>
                  </Box>
                }
              />
              <ListItemSecondaryAction>
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                  {version.status !== 'active' && (
                    <Button
                      size="small"
                      startIcon={<PlayArrowIcon />}
                      onClick={() => handleSetActive(version.id)}
                      sx={{
                        minWidth: 'auto',
                        p: 0.5,
                        color: '#00ff00',
                        '&:hover': {
                          backgroundColor: '#00ff0020',
                        },
                      }}
                    >
                      Активировать
                    </Button>
                  )}
                  <Button
                    size="small"
                    startIcon={<EditIcon />}
                    sx={{
                      minWidth: 'auto',
                      p: 0.5,
                      color: '#0066cc',
                      '&:hover': {
                        backgroundColor: '#0066cc20',
                      },
                    }}
                  >
                    Редактировать
                  </Button>
                  <Button
                    size="small"
                    startIcon={<DeleteIcon />}
                    sx={{
                      minWidth: 'auto',
                      p: 0.5,
                      color: '#ff0000',
                      '&:hover': {
                        backgroundColor: '#ff000020',
                      },
                    }}
                  >
                    Удалить
                  </Button>
                </Box>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>

        {versions.length > 5 && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Button
              variant="outlined"
              size="small"
              sx={{
                borderColor: '#555',
                color: '#cccccc',
                '&:hover': {
                  borderColor: '#777',
                  backgroundColor: '#404040',
                },
              }}
            >
              Показать все ({versions.length})
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

