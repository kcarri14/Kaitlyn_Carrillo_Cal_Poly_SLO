/** A scheduled action to be carried out by a specific entity. */
public abstract class Action {
    private final EntityAnimation entity;
    private final World world;
    private final ImageLibrary imageLibrary;
    private int repeatCount;

    public Action(EntityAnimation entity, World world, ImageLibrary imageLibrary, int repeatCount) {
        this.entity = entity;
        this.world = world;
        this.imageLibrary = imageLibrary;
        this.repeatCount = repeatCount;
    }

    /** Performs 'Behavior' specific logic. */
    public abstract void execute(EventScheduler scheduler);

    public EntityAnimation getEntity(){
        return entity;
    }

    public World getWorld(){
        return world;
    }

    public ImageLibrary getImageLibrary(){
        return imageLibrary;
    }

    public int getRepeatCount(){
        return repeatCount;
    }
}
