import { useRef, useCallback } from 'react';
import { confirmDialog } from 'primereact/confirmdialog';

/**
 * Custom hook for managing confirmation dialogs
 * Provides a consistent interface for showing confirmation dialogs
 */
export const useConfirmDialog = () => {
    const dialogRef = useRef(null);

    const confirm = useCallback((options = {}) => {
        const {
            message = 'Are you sure you want to proceed?',
            header = 'Confirmation',
            icon = 'pi pi-exclamation-triangle',
            accept,
            reject,
            acceptLabel = 'Yes',
            rejectLabel = 'No',
            acceptClassName = 'p-button-danger',
            rejectClassName = 'p-button-text',
            ...otherOptions
        } = options;

        return new Promise((resolve) => {
            confirmDialog({
                message,
                header,
                icon,
                acceptLabel,
                rejectLabel,
                acceptClassName,
                rejectClassName,
                accept: () => {
                    accept?.();
                    resolve(true);
                },
                reject: () => {
                    reject?.();
                    resolve(false);
                },
                ...otherOptions
            });
        });
    }, []);

    const confirmDelete = useCallback((itemName = 'item', options = {}) => {
        return confirm({
            message: `Are you sure you want to delete this ${itemName}? This action cannot be undone.`,
            header: 'Delete Confirmation',
            icon: 'pi pi-trash',
            acceptLabel: 'Delete',
            acceptClassName: 'p-button-danger',
            ...options
        });
    }, [confirm]);

    const confirmBulkDelete = useCallback((count, itemType = 'items', options = {}) => {
        return confirm({
            message: `Are you sure you want to delete ${count} ${itemType}? This action cannot be undone.`,
            header: 'Bulk Delete Confirmation',
            icon: 'pi pi-trash',
            acceptLabel: `Delete ${count} ${itemType}`,
            acceptClassName: 'p-button-danger',
            ...options
        });
    }, [confirm]);

    const confirmAction = useCallback((action, options = {}) => {
        const actionConfigs = {
            start: {
                message: 'Are you sure you want to start this investigation?',
                header: 'Start Investigation',
                icon: 'pi pi-play',
                acceptLabel: 'Start',
                acceptClassName: 'p-button-success'
            },
            stop: {
                message: 'Are you sure you want to stop this investigation?',
                header: 'Stop Investigation',
                icon: 'pi pi-stop',
                acceptLabel: 'Stop',
                acceptClassName: 'p-button-warning'
            },
            restart: {
                message: 'Are you sure you want to restart this investigation? Current progress will be lost.',
                header: 'Restart Investigation',
                icon: 'pi pi-refresh',
                acceptLabel: 'Restart',
                acceptClassName: 'p-button-warning'
            },
            cancel: {
                message: 'Are you sure you want to cancel this investigation?',
                header: 'Cancel Investigation',
                icon: 'pi pi-times',
                acceptLabel: 'Cancel',
                acceptClassName: 'p-button-danger'
            },
            export: {
                message: 'Do you want to export this investigation data?',
                header: 'Export Investigation',
                icon: 'pi pi-download',
                acceptLabel: 'Export',
                acceptClassName: 'p-button-info'
            },
            save: {
                message: 'Do you want to save your changes?',
                header: 'Save Changes',
                icon: 'pi pi-save',
                acceptLabel: 'Save',
                acceptClassName: 'p-button-success'
            },
            discard: {
                message: 'Are you sure you want to discard your changes?',
                header: 'Discard Changes',
                icon: 'pi pi-times',
                acceptLabel: 'Discard',
                acceptClassName: 'p-button-danger'
            },
            logout: {
                message: 'Are you sure you want to log out?',
                header: 'Logout',
                icon: 'pi pi-sign-out',
                acceptLabel: 'Logout',
                acceptClassName: 'p-button-secondary'
            }
        };

        const config = actionConfigs[action] || {};
        return confirm({ ...config, ...options });
    }, [confirm]);

    const confirmUnsavedChanges = useCallback((options = {}) => {
        return confirm({
            message: 'You have unsaved changes. Are you sure you want to leave this page?',
            header: 'Unsaved Changes',
            icon: 'pi pi-exclamation-triangle',
            acceptLabel: 'Leave',
            rejectLabel: 'Stay',
            acceptClassName: 'p-button-danger',
            ...options
        });
    }, [confirm]);

    const confirmNavigation = useCallback((destination, options = {}) => {
        return confirm({
            message: `Are you sure you want to navigate to ${destination}? Any unsaved changes will be lost.`,
            header: 'Navigate Away',
            icon: 'pi pi-exclamation-triangle',
            acceptLabel: 'Navigate',
            rejectLabel: 'Stay',
            acceptClassName: 'p-button-warning',
            ...options
        });
    }, [confirm]);

    // Custom confirmation dialog with input
    const confirmWithInput = useCallback((options = {}) => {
        const {
            message = 'Please confirm your action',
            header = 'Confirmation Required',
            inputLabel = 'Type "CONFIRM" to proceed:',
            expectedInput = 'CONFIRM',
            caseSensitive = false,
            ...otherOptions
        } = options;

        return new Promise((resolve) => {
            let inputValue = '';
            
            confirmDialog({
                message: (
                    <div>
                        <p>{message}</p>
                        <div className="p-field mt-3">
                            <label htmlFor="confirm-input">{inputLabel}</label>
                            <input
                                id="confirm-input"
                                type="text"
                                className="p-inputtext p-component w-full mt-1"
                                onChange={(e) => {
                                    inputValue = e.target.value;
                                }}
                                autoFocus
                            />
                        </div>
                    </div>
                ),
                header,
                icon: 'pi pi-exclamation-triangle',
                acceptLabel: 'Confirm',
                rejectLabel: 'Cancel',
                acceptClassName: 'p-button-danger',
                accept: () => {
                    const input = caseSensitive ? inputValue : inputValue.toLowerCase();
                    const expected = caseSensitive ? expectedInput : expectedInput.toLowerCase();
                    
                    if (input === expected) {
                        resolve(true);
                    } else {
                        // Show error and keep dialog open
                        setTimeout(() => {
                            confirmWithInput(options).then(resolve);
                        }, 100);
                    }
                },
                reject: () => {
                    resolve(false);
                },
                ...otherOptions
            });
        });
    }, []);

    const setDialogRef = useCallback((ref) => {
        dialogRef.current = ref;
    }, []);

    return {
        confirm,
        confirmDelete,
        confirmBulkDelete,
        confirmAction,
        confirmUnsavedChanges,
        confirmNavigation,
        confirmWithInput,
        setDialogRef,
        dialogRef
    };
};

export default useConfirmDialog;