from hooks import HookPoint, Hook

# example hooks for a pytorch "trainer". I'll generalize it from here.
# - For now all these hooks can be a type which can be specified by
#   the class on which the hooks are to be applied.
# - They can all inherit from a type like PostEpochHook, or PreBatchHook
# - Which would define their arguments or even default arguments.
# - After which the properties can be queried and a new hook added


def default_pre_batch_hook():
    pass


def default_pre_epoch_hook():
    pass


# default hooks. Logs the losses/accuracies and validates/tests the model
class DefaultPostEpochHook(Hook):
    def __call__(self, epoch, epoch_loss, old_epoch_loss, losses, logger):
        losses.append(('train', epoch, epoch_loss))
        logger.info("Cur epoch loss " + str(float(epoch_loss)) +
                    ", Prev epoch loss " + str(float(old_epoch_loss)))


class DefaultPostBatchHook(Hook):
    def __call__(self, print_interval, batch_num, logger, running_loss, epoch):
        reset = False
        if print_interval > 0 and (batch_num + 1) % print_interval == 0:
            logger.info('epoch %d, batch %d, loss: %.3f' %
                        (epoch + 1, batch_num + 1, running_loss))
            logger.debug('Reset running loss')
            reset = True
        return reset


class AdjustLRHook(Hook):
    def __call__(self, logger, adjust_lr_init_epoch, epoch, epoch_loss, old_epoch_loss, optimizer):
        if (epoch > adjust_lr_init_epoch and
                (old_epoch_loss - epoch_loss > (.01 * old_epoch_loss))):
            for param_group in optimizer.param_groups:
                param_group['lr'] *= .8
            logger.info("Annealing...")


class ChangeImageScaleHook(Hook):
    def __call__(self, epoch, set_temperature, change_scale_epoch, logger):
        if epoch > change_scale_epoch:
            temp = epoch // change_scale_epoch
            logger.debug("Setting temperature to %d" % temp)
            if (epoch + 1) % change_scale_epoch == 0:
                set_temperature(temp)


class SaveHook(Hook):
    def __call__(self, epoch, save_checkpoint, save_weights, save_interval):
        if (epoch + 1) % save_interval == 0:
            save_weights(epoch)
        save_checkpoint(epoch)


def validate_hook(hook_point):
    hp = hook_point
    if hp.args.val_freq > 0 and (hp.epoch % hp.args.val_freq == (hp.args.val_freq - 1)):
        if hp.val_loader:
            hp.validate(hp.epoch)


def test_hook(hook_point):
    hp = hook_point
    if hp.args.test_freq > 0 and (hp.epoch % hp.args.test_freq ==
                                  (hp.args.test_freq - 1)):
        if hp.test_loader:
            hp.test_model(hp.epoch)


def init_hook():
    # Currently None
    pass


class TrainerHookPoint(HookPoint):
    def __init__(self, trainer):
        super().__init__(trainer)
        self._trainer = trainer

    @property
    def logger(self):
        return self._trainer.logger


class PostBatchHookPoint(TrainerHookPoint):
    def __init__(self, trainer):
        super().__init__(trainer)
        self._batch_num = None
        self._running_loss = None

    @property
    def print_interval(self):
        return self._trainer.args.print_interval

    @property
    def batch_num(self):
        return self._batch_num

    @property
    def running_loss(self):
        return self._running_loss

    @property
    def epoch(self):
        return self._epoch

    def update(self, epoch, batch_num, running_loss):
        self._epoch = epoch
        self._batch_num = batch_num
        self._running_loss = running_loss


class Trainer:
    pass
